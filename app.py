from flask import Flask

app = Flask(__name__)


# 修改视图函数返回值、URL规则

@app.route('/home')
@app.route('/')
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


#自定义一些虚拟数据，渲染模板
name = 'snowtower ma'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


from flask import render_template

@app.route('/index')
def index():
    return render_template('index.html',name=name,movies=movies)

#url_for() 函数的用法，传入端点值（视图函数的名称）和参数，它会返回对应的 URL。
#对于静态文件，需要传入的端点值是 static，同时使用 filename 参数来传入相对于 static 文件夹的文件路径。


#数据库配置
import os
import sys

from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# Flask 提供了一个统一的接口来写入和获取这些配置变量：Flask.config 字典
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 创建数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


#编写一个自定义命令来自动执行创建数据库表操作
import click

@app.cli.command()
@click.option('--drop',is_flag=True, help="create after drop.")
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


#从数据库中读取数据
@app.route('/indexsql')
def indexsql():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user=user,movies=movies)


# 编写一个命令函数，将虚拟数据添加到数据库
@app.cli.command()
def forge():
    """Generate fake data."""
    #db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'laoma'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

#使用 app.errorhandler() 装饰器注册一个错误处理函数
# @app.errorhandler(404) # 传入要处理的错误代码
# def page_not_found(e): # 接受异常对象作为参数
#     user = User.query.first()
#     return render_template('404.html',user=user), 404


# 对于多个模板内都需要使用的变量
# 使用 app.context_processor 装饰器注册一个模板上下文处理函数
# 返回的变量（字典键值对形式）将会统一注入到每一个模板的上下文环境中，可以直接在模板中使用。
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user) #返回字典，等同于 return {'user': user}

# 因此更新404错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

