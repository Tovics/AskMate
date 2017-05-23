from flask import Flask, request, render_template
import import_from_questions
from datetime import datetime
import os.path
import base64
import psycopg2
import sql_queries


app = Flask(__name__)


@app.route('/')
def list_questions():
    return render_template('list.html', question_list=sql_queries.import_questions_from_db())


@app.route('/addquestion')
def render_question():
    return render_template('form.html')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    questions_details = sql_queries.import_single_question_from_db(question_id)
    date = questions_details[0][1]
    title = questions_details[0][4]
    question_id = questions_details[0][0]
    answer = ''
    question_description = questions_details[0][5]

    if request.method == 'POST':
        answer = request.form["answer"]
        return render_template('display.html', question_id=question_id, date=date, message=question_description, title=title)
    else:
        sql_queries.insert_answer(date, vote_number=0, answer='', image='')
        return render_template('display.html', question_id=question_id, date=date, message=question_description, title=title)


@app.route("/question", methods=['POST'])
def add_question():
    question_title = request.form["question_title"]
    question_description = request.form["question_description"]
    # questions_list = import_from_file()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if questions_list == []:
        question_id = 1
    else:
        question_id = int(questions_list[len(questions_list) - 1][0]) + 1
    if len(question_title) < 10:
        return render_template('form.html', msg='You should write longer question title! (Dumbass)')
    else:
        with open('questions.csv', 'a') as file_content:
            file_content.write(str(question_id) + ", " + question_title +
                               ", " + question_description + ", " + date + '\n')
        return render_template('list.html', question_list=import_from_file())


"""def import_from_file(file_name="questions.csv"):
    questions_list = []
    with open(file_name, "r") as file_content:
        questions = file_content.readlines()
    for i in questions:
        questions_list.append(i.replace('\n', '').split(', '))
    return questions_list"""


def main():
    app.run(debug=True)
    import_from_file()


if __name__ == '__main__':
    main()
