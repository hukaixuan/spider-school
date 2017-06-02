from flask import Flask, render_template, request
from answer import process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dosomething', methods=['POST'])
def dosomething():
    username = request.form.get('username')
    password = request.form.get('password')
    return process(username, password)
    

if __name__ == '__main__':
    app.run()