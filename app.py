from flask import Flask 
from flask import render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql


app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:9625@localhost:3306/register"
db = SQLAlchemy(app)

class colbert_registersapp(db.Model):
    registerld = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    id = db.Column(db.String(255))
    phonenum = db.Column(db.String(255))
    password = db.Column(db.String(255))
    password_hint = db.Column(db.String(255))
    email = db.Column(db.String(255))
    
    
    def __repr__(self): 
        return "registerld: {0} | name: {1} | id: {2} | phonenum: {3} | password: {4} | password_hint: {5} | email: {6}".format(self.registerld, self.name, self.id, self.phonenum,
                                                                                                                        self.password, self.password_hint, self.email )




class RegisterForm(FlaskForm):
    registerld = IntegerField('Regiseterld ID:')
    name = StringField('Name:', validators=[DataRequired()])
    id = StringField('Id:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    password_hint = StringField('Password_hint:', validators=[DataRequired()])
    phonenum = StringField('Phonenum:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])


# @app.route('/')
# def index():
#     return render_template('index.html', pageTitle='MyPage')

@app.route('/')
def index():
    all_regiseters = colbert_registersapp.query.all()
    return render_template('index.html', registers=all_regiseters, pageTitle='모든 회원 데이터베이스', )
   

@app.route('/add_register', methods=['GET', 'POST'])
def add_register():
    form = RegisterForm()
    if form.validate_on_submit():
        register = colbert_registersapp(name=form.name.data, id= form.id.data, password = form.password.data, 
                                   password_hint=form.password_hint.data, phonenum=form.phonenum.data, email=form.email.data)
        db.session.add(register)
        db.session.commit()
        return redirect('/')
      
    return render_template('add_register.html', form=form, pageTitle='회원등록하기')



@app.route('/delete_register/<int:member_id>', methods=['GET','POST'])
def delete_register(member_id):
    if request.method == 'POST': # 만약 POST를 요청 받을 시, 데이터베이스에서 친구를 삭제한다 
        register = colbert_registersapp.query.get_or_404(member_id)
        db.session.delete(register)
        db.session.commit()
        return redirect('/')
    else: # 만약 GET을 요청 받을 시, 메인페이지로 보내준다.
        return redirect('/')


@app.route('/register/register/<int:member_id>', methods=['GET','POST'])
def get_register(member_id):
    register = colbert_registersapp.query.get_or_404(member_id)
    return render_template('register.html', form=register, pageTitle='회원정보 세부사항', legend="회원정보 세부사항")

@app.route('/register/register/<int:member_id>/update', methods=['GET','POST'])
def update_register(member_id):
    register = colbert_registersapp.query.get_or_404(member_id)
    form = RegisterForm()

    if form.validate_on_submit():
        register.name = form.name.data
        register.id = form.id.data
        register.phonenum = form.phonenum.data
        register.password = form.password.data
        register.password_hint = form.password_hint.data
        register.email = form.email.data
        db.session.commit()
        return redirect(url_for('get_register', member_id=register.registerld))
    form.registerld.data = register.registerld
    form.name.data = register.name
    form.id.data = register.id
    form.phonenum.data = register.phonenum
    form.password.data = register.password
    form.password_hint.data = register.password_hint
    form.email.data = register.email
    return render_template('update_register.html', form=form, pageTitle='Update Friend', legend="Update A Friend")




if __name__ == '__main__':
    app.run(debug=True)
