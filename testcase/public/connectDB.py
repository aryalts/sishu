# -*- coding:utf8 -*-
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
import pymongo



def conmysql(sql):
    server = SSHTunnelForwarder(
        ssh_address_or_host=('10.68.100.137', 22),
        ssh_password='password',
        ssh_username='root',
        remote_bind_address=('172.20.3.145', 3306))

    server.start()

    conn = pymysql.connect(
        host='127.0.0.1',  # 这里固定
        port=server.local_bind_port,
        user='dba_admin',
        passwd='Dba.net2018',
        db='sso')
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchone()
            return data

    except Exception as e:
        print(e)
    finally:
        conn.close()


# def conmongodb(data):
#     client = pymongo.MongoClient(host='10.68.100.54', port=27017)
#     db = client.recruit
#     collection1 = db.teachers
#     collection1.del({"email":data})
#     collection2 = db.remuses
#     collection2.remobe({"email":data})

def conmongodb(data):
    myclient = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
    mydb = myclient["recruit"]
    mycol1 = mydb["teachers"]
    mycol1.delete_one({'email':data})
    mycol2 = mydb["resumes"]
    mycol2.delete_one({'email':data})



