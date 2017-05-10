from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def hali():
    return render_template('form.html')


@app.route("/question", methods=['POST'])
def add_question():
    question = request.form['question']
    if len(question) < 10:
        return render_template('form.html', msg='You should write longer idiot.')
    else:
        with open('questions.csv', 'a') as file_content:
            file_content.write(question)
        return render_template('form.html', msg='motherfucker')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
