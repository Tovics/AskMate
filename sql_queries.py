import psycopg2


def import_questions_from_db():
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question;""")
    question_list = cursor.fetchall()
    return question_list


def import_answers_from_db(question_id):
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    # question_id = int(question_id)
    cursor.execute("""SELECT * FROM answer WHERE id=%s;""", (question_id,))
    answer = cursor.fetchall()
    return answer


def import_single_question_from_db(question_id):
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question WHERE id=%s;""", (question_id,))
    question = cursor.fetchall()
    return question


def insert_answer(date, vote_number, answer, image):
    connect_str = "dbname='zsofi' user='zsofi' host='localhost' password='pwd'"
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, message, image)
                            VALUES (%s, %s, %s, %s);""", (date, vote_number, answer, image))


def main():
    import_questions_from_db()


if __name__ == '__main__':
    main()
