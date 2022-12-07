from flask import Flask, render_template, request,session,redirect,url_for
import pymysql, hashlib
from adda import Adda
app = Flask(__name__)
app.secret_key = Adda().get_secret_key()

@app.route('/',methods=['POST','GET'])
def home():
    return render_template('test.html')

def log(user_id, api_uri, method):
    Adda().log(user_id ,api_uri, method)

# 로그인
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pass_receive = request.form['pass_give']

    print(id_receive)
    print(pass_receive)

    # result = hashlib.sha256(pass_receive.encode())

    user={
        'id' : id_receive,
        'pass' : pass_receive
    }
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='ghjr1178!',
                         db='sparta_test',
                         charset='utf8'
                         )

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('use sparta_test;')
    cursor.execute(
        f'select * from student where userid = "{id_receive}"')
    user = cursor.fetchone()

    print(user)

    if user == None:
        return '유저가 없습니다'
    if user and user["password"] == pass_receive:
        print('로그인 완료!')
    if user and user["password"] != pass_receive:
        print('비밀번호가 틀렸습니다.')

    if user:
        session['id'] = id_receive
        db.commit()
        db.close()
        return redirect(url_for('home'))
    db.commit()
    db.close()

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('userid',None)
    return render_template("index.html")

# 서버실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)