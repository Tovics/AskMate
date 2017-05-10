from flask import Flask, request, render_template
import import_from_questions
app = Flask(__name__)


@app.route('/')
def hali():
    return render_template('form.html')


@app.route("/question", methods=['POST'])
def add_question():
    question_title = request.form["question_title"]
    question_description = request.form["question_description"]
    questions_list = import_from_file()
    if questions_list is None:
        question_ID = 1
    else:
        question_ID = int(questions_list[len(questions_list)-1][0])+1
    if len(question_title) < 10:
        return render_template('form.html', msg='You should write longer question title! (Dumbass)')
    else:
        with open('questions.csv', 'a') as file_content:
            file_content.write(str(question_ID) + ", " + question_title + '\n')
        return render_template('form.html', msg=question_title)


def import_from_file(file_name="questions.csv"):
    questions_list = []
    with open(file_name, "r") as file_content:
        questions = file_content.readlines()
    for i in questions:
        questions_list.append(i.replace('\n', '').split(', '))
    return questions_list


def main():
    app.run(debug=True)
    import_from_file()

if __name__ == '__main__':
    main()
