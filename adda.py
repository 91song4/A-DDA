import hashlib
import pymysql

class Adda:
    def __init__(self):
        self.__secret_key = 'NeedChange'
    
    def get_secret_key(self):
        return self.__secret_key
    
    def log(self,user_id, api_uri, method,):
        db=pymysql.connect(host='localhost',port=3306,user='root',password='123123',db='adda',charset='utf8')
    
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute('use adda;')    

        cursor.execute('show tables;')
        val = cursor.fetchall()
        flag = 0
        for i in val:
            if i['Tables_in_adda'] == 'log':
                flag = 1

        if flag == 0:
            cursor.execute('create table log(id int(11) primary key auto_increment, created datetime default current_timestamp, user_id varchar(20), api_uri varchar(20) not null, method varchar(20) not null, foreign key (user_id) reference user(id) on update cascade);')

        cursor.execute(f"insert into log (user_id, api_uri, method) values('{user_id}','{api_uri}','{method}')")

        db.commit()
        db.close()