import psycopg2


def import_questions_from_db():
    connect_str = "dbname='borzfele' user='borzfele' host='localhost' password='91december30'"
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question;""")
    question = cursor.fetchall()
    return question


def main():
    import_questions_from_db()

if __name__ == '__main__':
    main()