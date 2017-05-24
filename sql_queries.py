import psycopg2
from datetime import datetime


def import_questions_from_db():
<<<<<<< HEAD
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
=======
    connect_str = "dbname='borzfele' user='borzfele' host='localhost' password='91_december_30'"
>>>>>>> 5613693c5dc7b7d572d2fdcf5f2839459f5602bf
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question;""")
    question_list = cursor.fetchall()
    return question_list


def import_answers_from_db(question_id):
<<<<<<< HEAD
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
=======
    connect_str = "dbname='borzfele' user='borzfele' host='localhost' password='91_december_30'"
>>>>>>> 5613693c5dc7b7d572d2fdcf5f2839459f5602bf
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    # question_id = int(question_id)
    cursor.execute("""SELECT * FROM answer WHERE question_id=%s;""", (question_id,))
    answer = cursor.fetchall()
    return answer


def import_single_question_from_db(question_id):
<<<<<<< HEAD
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
=======
    connect_str = "dbname='borzfele' user='borzfele' host='localhost' password='91_december_30'"
>>>>>>> 5613693c5dc7b7d572d2fdcf5f2839459f5602bf
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question WHERE id=%s;""", (question_id,))
    question = cursor.fetchall()
    return question


def insert_question(title='', message='', view_number=0, vote_number=0, image=''):
<<<<<<< HEAD
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
=======
    connect_str = "dbname='borzfele' user='borzfele' host='localhost' password='91_december_30'"
>>>>>>> 5613693c5dc7b7d572d2fdcf5f2839459f5602bf
    conn = psycopg2.connect(connect_str)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                            VALUES (%s, %s, %s, %s, %s, %s);""", (date, view_number, vote_number, title, message, image))


def insert_answer(question_id, answer='', vote_number=0, image=''):
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
    conn = psycopg2.connect(connect_str)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                            VALUES (%s, %s, %s, %s, %s);""", (date, vote_number, question_id, answer, image))


def sort_questions_asc(sort_by):
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question ORDER BY submission_time ASC;""", (question_id,))
    sort = cursor.fetchall()
    return sort


def main():
    pass


if __name__ == '__main__':
    main()
