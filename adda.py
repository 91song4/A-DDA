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

        cursor.execute(f"insert into log (user_id, api_uri, method) values('{user_id}','{api_uri}','{method}')")

        # str = 'test'
        # result = hashlib.sha256(str.encode())
        # cursor.execute(f"insert into user(id, password,selfname,phone ) values('id_test3','{result.hexdigest()}','name_test3','phone_test3')")
        # value = cursor.fetchall()
        # print(value)

        db.commit()
        db.close()