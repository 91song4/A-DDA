from adda import Adda
import pymysql
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)
app.secret_key = Adda().get_secret_key()

# 메인화면
@app.route('/')
def home():
    return render_template('01_main.html')

def log(user_id, api_uri, method):
    Adda().log(user_id, api_uri, method)

# 로그인화면
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    return render_template('02_login.html')

@app.route('/logout')
def logout():
    return redirect(url_for(''))

# 회원가입화면
@app.route('/signup')
def signup():
    return render_template('03_signup.html')

# 추가화면
@app.route('/about')
def about():
    return '김범석, 송지훈, 이호승, 전진영, 선승우'

# Aside
@app.route('/game')
def game():
    return render_template('04_game.html')

# mypage
@app.route('/mypage')
def mypage():
    return render_template('12_mypage.html')

# mypage
@app.route('/writting')
def writting():
    return render_template('13_writting.html')

@app.route('/login', methods=['GET', 'POST'])
def login_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    return jsonify({'result': 'success', 'msg': '로그인 성공'})

@app.route('/signup', methods=['GET', 'POST'])
def singup_get():
    id_receive = request.args.get('id_give')
    pw_receive = request.args.get('pw_give')
    return jsonify({'result': 'success', 'msg': '회원가입완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)