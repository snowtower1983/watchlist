from flask import Flask

app = Flask(__name__)


# 修改视图函数返回值、URL规则

@app.route('/home')
@app.route('/')
@app.route('/index')
def hello():
    return "Welcome to Flask World."

@app.route('/totoro')
def helloTotoro():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

#URL中定义变量
@app.route('/user/<name>')
def user_page(name):
    return name+"'s private page."

#获取变量的安全方式
#使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理
#不做代码执行
from markupsafe import escape

@app.route('/random/<input>')
def solve_random_input(input):
    return f'what do you want with {escape(input)}'

#作为代表某个路由的端点（endpoint），同时用来生成视图函数对应的 URL
#Flask 提供了一个 url_for 函数来生成 URL，它接受的第一个参数就是端点值
from flask import url_for

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'
