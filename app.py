import app as app
from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql, hashlib

from adda import Adda

# app.secret_key = Adda().get_secret_key()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123123@localhost:3306/register"
db = SQLAlchemy(app)


class user(db.Model):
    memberid = db.Column(db.Integer, primary_key = True)
    ID = db.Column(db.String(255))
    password = db.Column(db.String(255))
    selfname = db.Column(db.String(255))
    phone = db.Column(db.String(255))

   
# 메인화면
@app.route('/')
def home():
    print('home() access')
    print(session)
    if 'id' in session:
        return  render_template('11_main_login.html')
    return render_template('01_main.html')

class RegisterForm(FlaskForm):
    memberid = IntegerField('Memberid ID:')
    ID = StringField('id:', validators=[DataRequired()])
    password = StringField('PASSWORD:', validators=[DataRequired()])
    selfname = StringField('SELFNAME:', validators=[DataRequired()])
    phone = StringField('PHONE:', validators=[DataRequired()])


def log(user_id, api_uri, method):
    Adda().log(user_id, api_uri, method)


# 로그인화면
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('02_login.html')


@app.route('/logout')
def logout():
    return redirect(url_for(''))


# 회원가입화면
# @app.route('/signup')
# def signup():
#     return render_template('03_signup.html')


# 추가화면
@app.route('/about')
def about():
    return '김범석, 송지훈, 이호승, 전진영, 선승우'


# Aside
@app.route('/game')
def game():
    return render_template('04_game.html')


# mypage
# @app.route('/mypage')
# def mypage():
#     return render_template('12_mypage.html')


# mypage
@app.route('/writting')
def writting():
    return render_template('13_writting.html')
   

# 회원가입 구현 

@app.route('/mypage')
def index():
    all_regiseters = user.query.all()
    return render_template('index.html', registers=all_regiseters, pageTitle='모든 회원 데이터베이스', )

@app.route('/add_register', methods=['GET', 'POST'])
def add_register():
    form = RegisterForm()
    if form.validate_on_submit():
        register = user(ID=form.ID.data, password=form.password.data, selfname= form.selfname.data, phone = form.phone.data)
        db.session.add(register)
        db.session.commit()
        return redirect('/')
      
    return render_template('add_register.html', form=form, pageTitle='회원등록하기')



@app.route('/delete_register/<int:member_id>', methods=['GET','POST'])
def delete_register(member_id):
    if request.method == 'POST': # 만약 POST를 요청 받을 시, 데이터베이스에서 친구를 삭제한다 
        register = user.query.get_or_404(member_id)
        db.session.delete(register)
        db.session.commit()
        return redirect('/')
    else: # 만약 GET을 요청 받을 시, 메인페이지로 보내준다.
        return redirect('/')


@app.route('/register/register/<int:member_id>', methods=['GET','POST'])
def get_register(member_id):
    register = user.query.get_or_404(member_id)
    return render_template('register.html', form=register, pageTitle='회원정보 세부사항', legend="회원정보 세부사항")

@app.route('/register/register/<int:member_id>/update', methods=['GET','POST'])
def update_register(member_id):
    register = user.query.get_or_404(member_id)
    form = RegisterForm()
    
    if form.validate_on_submit():
        register.ID = form.ID.data
        register.password = form.password.data
        register.selfname = form.selfname.data
        register.phone = form.phone.data
        db.session.commit()
        return redirect(url_for('get_register', member_id=register.memberid))
    form.memberid.data = register.memberid
    form.ID.data = register.ID
    form.password.data = register.password
    form.selfname.data = form.selfname
    form.phone.data = register.phone
    return render_template('update_register.html', form=form, pageTitle='Update Friend', legend="Update A Friend")


@app.route('/api/user_img_upload', methods=['POST'])
def api_usr_img_upload():
    print(request.method)
    # if request.method == 'POST':
    f = request.files['file']
    extension = f.filename.split('.')[-1]
    print(f.filename.split('.'))
    filename = f'{session["id"]}.{extension}'
    print(filename)
    f.save(f'static/profile_image/{filename}')

    db = pymysql.connect(host='localhost',port=3306,user='root',password='123123',db='adda',charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('use adda;')
    cursor.execute(f'update user set profile = "{filename}" where id = "{session["id"]}";')

    db.commit()
    db.close()
    
    return redirect(url_for('mypage'))


@app.route('/api/user_img_load', methods=['GET'])
def api_user_img_load():
    print('api user img load() access')
    db = pymysql.connect(host='localhost',port=3306,user='root',password='123123',db='adda',charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('use adda;')
    cursor.execute(f'select profile from user where id = "{session["id"]}";')
    user_img = cursor.fetchone()

    db.commit()
    db.close()
    return user_img['profile']

# 로그인
@app.route('/api/login', methods=['POST'])
def api_login():
    if 'id' in session:
        Adda().log(session['id'], '/api/login', 'POST')
    print('api_login() access')

    id_receive = request.form['id_give']
    pass_receive = request.form['pass_give']

    print(id_receive)
    print(pass_receive)

    # result = hashlib.sha256(pass_receive.encode())

    # user={
    #     'id' : id_receive,
    #     'pass' : pass_receive
    # }
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='123123',
                         db='adda',
                         charset='utf8'
                         )

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        f'select * from user where id = "{id_receive}"')
    user = cursor.fetchone()

    print(user)

    if user == None:
        print('유저가 없습니다.')
        db.close()
        return '유저가 없습니다.'
    elif user and user["password"] != pass_receive:
        print('비밀번호가 틀렸습니다.')
        db.close()
        return '비밀번호가 없습니다.'
    elif user and user["password"] == pass_receive:
        print('로그인 완료!')
        session['id'] = id_receive
        db.commit()
        db.close()
        return redirect(url_for('home'))


# 로그아웃
@app.route('/api/logout')
def api_logout():
    if 'id' in session:
        print(session)
        Adda().log(session['id'], '/api/logout', 'GET')
    session.clear()
    return redirect(url_for('home'))

# 서버실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)