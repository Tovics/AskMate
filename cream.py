from flask import Flask, request, render_template, redirect, url_for
import import_from_questions
from datetime import datetime
import os.path
import base64
import psycopg2
import sql_queries


app = Flask(__name__)


@app.route('/users')
def list_users():
    return render_template('user_list.html', user_list=sql_queries.import_users_from_db())


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


@app.route('/search', methods=['GET', 'POST'])
def search_questions():
    search_request = request.form["search"]
    search_request = search_request.lower()
    search_results = sql_queries.search_in_questions(search_request)
    return render_template('list.html', search_results=search_results)


@app.route('/addquestion')
def render_question():
    return render_template('form.html', users_ordered=sql_queries.import_users_from_db_ordered())


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


@app.route('/question/<question_id>/delete_answer/<answer_id>', methods=['GET', 'POST'])
def delete_answer(question_id, answer_id):
    sql_queries.delete_answer(question_id, answer_id)
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    questions_details = sql_queries.import_single_question_from_db(question_id)
    answer_details = sql_queries.import_answers_from_db(question_id)
    question_comments = sql_queries.import_comments_for_question(question_id)
    answer_comment = sql_queries.import_comments_for_answer()
    question_date = questions_details[0][1]
    question_title = questions_details[0][4]
    question_id = int(questions_details[0][0])
    question_description = questions_details[0][5]
    users_ordered = sql_queries.import_users_from_db_ordered()
    if request.method == 'POST':
        answer = request.form["answer"]
        users_name_answ = request.form["users_name_answ"]
        users_id_answ = sql_queries.import_single_user_from_db_answ_bind(users_name_answ)
        sql_queries.insert_answer(question_id, answer, users_id_answ)
        return redirect('/question/{}'.format(question_id))
    else:
        return render_template('display.html', question_id=question_id, date=question_date, message=question_description, title=question_title, answer_details=answer_details, comments=question_comments, users_ordered=users_ordered, answer_comment=answer_comment)


@app.route("/question", methods=['POST'])
def add_question():
    question_title = request.form["question_title"]
    question_description = request.form["question_description"]
    users_name = request.form["users_name"]
    users_id = sql_queries.import_single_user_from_db_ordered(users_name)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql_queries.insert_question(question_title, question_description, users_id)
    return render_template('list.html', question_list=sql_queries.import_questions_from_db())


@app.route("/answer/<answer_id>/accept")
def accept_answer(answer_id):
    sql_queries.accept_answer(answer_id)
    return redirect('/')


@app.route("/vote_up/<question_id>")
def vote_up(question_id):
    sql_queries.vote_up(question_id)
    return redirect('/')


@app.route("/vote_down/<question_id>")
def vote_down(question_id):
    sql_queries.vote_down(question_id)
    return redirect('/')


@app.route("/registration")
def register():
    return render_template('registration.html')


@app.route("/add_user_to_db", methods=['POST'])
def add_user():
    username = request.form["username"]
    registration_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql_queries.create_user(username, registration_time)
    return render_template('registration.html')


@app.route("/user/<user_id>")
def display_user(user_id):
    return render_template('user_display.html', user_details=sql_queries.import_single_user_from_db(user_id))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    comment = request.form["comment"]
    users_name_comm = request.form["users_name_comm"]
    users_id = sql_queries.import_single_user_from_db_comm_bind(users_name_comm)
    sql_queries.add_comment_to_question(question_id, comment, users_id)
    return redirect("/question/{}".format(question_id))


@app.route("/question/<question_id>/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id, question_id):
    comment = request.form["answer_comment_textarea"]
    users_name_answer_comment = request.form["users_name_ans_comm"]
    users_id = sql_queries.import_single_user_from_db_comm_bind(users_name_answer_comment)
    sql_queries.add_comment_to_answer(question_id, answer_id, users_id, comment)
    return redirect("/question/{}".format(question_id))


def main():
    app.run(debug=True)
    import_from_file()


if __name__ == '__main__':
    main()
