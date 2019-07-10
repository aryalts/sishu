# -*- coding:utf8 -*-
import pymysql.cursors
import datetime,time

config = {
    'host': '10.68.100.125',
    'port': 3306,
    'user': 'root',
    'password': 'uuabc@123',
    'db': 'teacher_contract'
}


db = pymysql.connect(**config)
# test1 = '2019-05-01 00:00:00'
# # string格式的时间转为元组
# test2 = time.strptime(test1, "%Y-%m-%d %H:%M:%S")
# # 元组格式的时间转为时间戳
# test3 = int(time.mktime(test2))
# # 元组格式的时间转为string
# test4 = time.strftime("%Y-%m-%d %H:%M:%S", test2)

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


