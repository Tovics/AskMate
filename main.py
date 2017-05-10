from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def hali():
    return render_template('form.html')


@app.route("/question", methods=['POST'])
def add_question():
    return render_template('form.html', msg = 'You should write longer idiot.')


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
