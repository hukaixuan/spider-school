from flask import Flask, render_template, request
from tasks import exam, add

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dosomething', methods=['POST'])
def dosomething():
    username = request.form.get('username')
    password = request.form.get('password')
    exam.delay(username, password)
    return '<p>自动答题任务已加入队列。。。几分钟后去教务系统看下吧</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8999)
