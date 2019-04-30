# -*- coding:utf8 -*-
import pymysql.cursors

config = {
    'host': '10.68.100.125',
    'port': 3306,
    'user': 'root',
    'password': 'uuabc@123',
    'db': 'teacher_contract'
}


db = pymysql.connect(**config)

try:
    with db.cursor() as cursor:
        sql = """select * FROM signed_time where teacher_id = %s"""
        cursor.execute(sql, 1424)
        data = cursor.fetchone()
        print(data)

except Exception as e:
    print(e)
finally:
    db.close()


