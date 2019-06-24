# -*- coding:utf8 -*-
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder

def connect_mysql(sql):
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

    except Exception as something_wrong:
        print(something_wrong)
    finally:
        conn.close()

def connect_mysql_qa(sql):

    conn = pymysql.connect(
        host='rm-bp15do63ws7rs648qvo.mysql.rds.aliyuncs.com',
        port=3306,
        user='qa',
        passwd='qa@UUabc',
        db='sso')
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchone()
            return data

    except Exception as something_wrong:
        print(something_wrong)
    finally:
        conn.close()





