import psycopg2

try:
    # setup connection string
    connect_str = "dbname='borzfele' user='borzfele' host='localhost' password='91december30'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # set autocommit option, to do every query when we call it
    conn.autocommit = True
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # removing the test table if it already exists
    cursor.execute("""DROP TABLE IF EXISTS connection_check;""")
    # create a new table with a single column called "name"
    cursor.execute("""CREATE TABLE connection_check (name varchar(40));""")
    # Insert a row to see something in the output
    cursor.execute("""INSERT INTO connection_check VALUES ('It works!');""")
    # run a SELECT statement
    cursor.execute("""SELECT * FROM connection_check;""")
    # Fetch and print the result of the last execution
    rows = cursor.fetchall()
    print(rows)
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
