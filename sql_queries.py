import psycopg2
from datetime import datetime


def connection_decorator(func):
    def func_wrapper(*args):
        connect_str = "dbname='tovics' user='tovics' host='localhost' password='88Szekér99'"
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
def import_questions_from_db(cursor):
    cursor.execute("""SELECT * FROM question;""")
    question_list = cursor.fetchall()
    return question_list


@connection_decorator
def import_answers_from_db(cursor, question_id):
    # question_id = int(question_id)
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
def insert_question(cursor, title='', message='', view_number=0, vote_number=0, image=''):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                            VALUES (%s, %s, %s, %s, %s, %s);""", (date, view_number, vote_number, title, message, image))


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


def main():
    pass

if __name__ == '__main__':
    main()
