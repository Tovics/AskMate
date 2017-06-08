import psycopg2
from datetime import datetime


def connection_decorator(func):
    def func_wrapper(*args):
        connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        return func(cursor, *args)
    return func_wrapper


@connection_decorator
def import_users_from_db(cursor):
    cursor.execute("""SELECT * FROM users;""")
    users_list = cursor.fetchall()
    return users_list


@connection_decorator
def import_users_from_db_ordered(cursor):
    cursor.execute("""SELECT name, id FROM users ORDER BY name ASC;""")
    users_list_ordered = cursor.fetchall()
    return users_list_ordered


@connection_decorator
def import_single_user_from_db_ordered(cursor, users_name):
    cursor.execute("""SELECT id FROM users WHERE name='{}';""".format(users_name))
    single_user = cursor.fetchall()
    single_user = single_user[0][0]
    return single_user


@connection_decorator
def import_single_user_from_db(cursor, user_id):
    cursor.execute("""
                    SELECT users.name, users.registration_time, question.title, answer.message, comment.message FROM users
                    LEFT JOIN question
                    ON users.id = question.users_id
                    LEFT JOIN answer
                    ON users.id = answer.users_id
                    LEFT JOIN comment
                    ON users.id = comment.users_id
                    WHERE users.id = {};
                    """.format(user_id))
    user_details = cursor.fetchall()
    return user_details


@connection_decorator
def import_questions_from_db(cursor):
    cursor.execute("""SELECT * FROM question;""")
    question_list = cursor.fetchall()
    return question_list


@connection_decorator
def import_answers_from_db(cursor, question_id):
    cursor.execute("""SELECT * FROM answer WHERE question_id=%s;""", (question_id,))
    answer = cursor.fetchall()
    return answer


@connection_decorator
def import_single_question_from_db(cursor, question_id):
    question_id = int(question_id)
    cursor.execute("""SELECT * FROM question WHERE id='%s';""", (question_id,))
    question = cursor.fetchall()
    return question


@connection_decorator
def insert_question(cursor, title='', message='', users_id=0, view_number=0, vote_number=0, image=''):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image, users_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);""", (date, view_number, vote_number, title, message, image, users_id))


@connection_decorator
def insert_answer(cursor, question_id, answer='', vote_number=0, image=''):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                            VALUES (%s, %s, %s, %s, %s);""", (date, vote_number, question_id, answer, image))


@connection_decorator
def update_question(cursor, question_id, title, message):
    cursor.execute("""UPDATE question SET title=%s, message=%s WHERE id=%s;""", (title, message, question_id))


@connection_decorator
def sort_questions(cursor, criterium, ordering):
    cursor.execute("""SELECT * FROM question ORDER BY {} {};""".format(criterium, ordering))
    sort = cursor.fetchall()
    return sort


@connection_decorator
def delete_question(cursor, question_id):
    question_id = int(question_id)
    cursor.execute("""DELETE FROM answer WHERE question_id='{}';""".format(question_id))
    cursor.execute("""DELETE FROM question WHERE id='{}';""".format(question_id))


@connection_decorator
def delete_answer(cursor, question_id, answer_id):
    question_id = int(question_id)
    answer_id = int(answer_id)
    cursor.execute("""DELETE FROM answer WHERE id={};""".format(answer_id))


@connection_decorator
def search_in_questions(cursor, search_request):
    search_request = search_request.lower()
    cursor.execute("""SELECT * FROM question WHERE title ILIKE '%{}%';""".format(search_request))
    search_results = cursor.fetchall()
    return search_results


@connection_decorator
def vote_up(cursor, question_id):
    cursor.execute("""SELECT vote_number FROM question WHERE id={};""".format(question_id))
    vote_number = cursor.fetchone()
    vote_number = int(vote_number[0])
    vote_number += 1
    cursor.execute("""UPDATE question SET vote_number='{}' WHERE id={};""".format(vote_number, question_id))


@connection_decorator
def vote_down(cursor, question_id):
    cursor.execute("""SELECT vote_number FROM question WHERE id={};""".format(question_id))
    vote_number = cursor.fetchone()
    vote_number = int(vote_number[0])
    vote_number -= 1
    cursor.execute("""UPDATE question SET vote_number='{}' WHERE id={};""".format(vote_number, question_id))


@connection_decorator
def create_user(cursor, name, registration_time):
    cursor.execute("""INSERT INTO users (name, registration_time)
                            VALUES (%s, %s);""", (name, registration_time))


@connection_decorator
def add_comment_to_question(cursor, question_id, message):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        """
        INSERT INTO comment
        (question_id, answer_id, message, submission_time, edited_count, users_id)
        VALUES (%s, NULL, %s, %s, NULL, NULL);
        """, (question_id, message, submission_time))


@connection_decorator
def import_comments_for_question(cursor, question_id):
    cursor.execute(
        """
        SELECT message, submission_time
        FROM comment
        WHERE question_id = {};
        """.format(question_id)
    )
    comment = cursor.fetchall()
    return comment


def main():
    print(import_single_user_from_db_ordered('Tarzan'))

if __name__ == '__main__':
    main()
