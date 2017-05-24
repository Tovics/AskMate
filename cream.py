from flask import Flask, request, render_template, redirect, url_for
import import_from_questions
from datetime import datetime
import os.path
import base64
import psycopg2
import sql_queries


app = Flask(__name__)


@app.route('/')
def list_questions():
    criterium = None
    ordering = None
    ordered = sql_queries.import_questions_from_db()
    for key in request.args:
        criterium = key
        ordering = request.args[key]
    if criterium and ordering:
        ordered = sql_queries.sort_questions(criterium, ordering)
    return render_template('list.html', question_list=ordered)


@app.route('/addquestion')
def render_question():
    return render_template('form.html')


@app.route('/edit_question/<question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question_id = int(question_id)
    question_details = sql_queries.import_single_question_from_db(question_id)
    if request.method == 'POST':
        sql_queries.update_question(question_id, request.form['question_title'], request.form['question_description'])
        return redirect(url_for('list_questions'))
    return render_template('form.html', question_details=question_details)


@app.route('/delete_question/<question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    question_id = int(question_id)
    sql_queries.delete_question(question_id)
    return redirect(url_for('list_questions'))


@app.route('/delete_answer/<question_id>', methods=['GET', 'POST'])
def delete_answer(question_id, answer_id):
    question_id = int(question_id)
    answer_id = int(answer_id)
    sql_queries.delete_answer(question_id, answer_id)
    return redirect(url_for('list_questions'))


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    questions_details = sql_queries.import_single_question_from_db(question_id)
    answer_details = sql_queries.import_answers_from_db(question_id)
    question_date = questions_details[0][1]
    question_title = questions_details[0][4]
    question_id = int(questions_details[0][0])
    question_description = questions_details[0][5]

    if request.method == 'POST':
        answer = request.form["answer"]
        sql_queries.insert_answer(question_id, answer)
        return redirect('/question/{}'.format(question_id))
    else:
        return render_template('display.html', question_id=question_id, date=question_date, message=question_description, title=question_title, answer_details=answer_details)


@app.route("/question", methods=['POST'])
def add_question():
    question_title = request.form["question_title"]
    question_description = request.form["question_description"]
    # questions_list = import_from_file()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql_queries.insert_question(question_title, question_description)
    return render_template('list.html', question_list=sql_queries.import_questions_from_db())


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
