from flask import Flask, render_template, request,session,redirect,url_for
import pymysql
from adda import Adda
app = Flask(__name__)
app.secret_key = Adda().get_secret_key()

@app.route('/',methods=['POST','GET'])
def home():
    return render_template('test.html')

def log(user_id, api_uri, method):
    Adda().log(user_id ,api_uri, method)

# 서버실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)