# -*- coding:utf8 -*-
import pymysql
import time


db = pymysql.connect("10.68.100.125","root","uuabc@123","teacher_contract")

cursor = db.cursor()

sql = """select * FROM signed_time where teacher_id = 1424"""

try:
    cursor.execute(sql)

    data = cursor.fetchall()

    for rows in data:
        id = rows[0]
        teacher_id = rows[1]
        weekday = rows[2]
        start_time = rows[3]
        end_time = rows[4]
        signed_id = rows[5]
        effective_start_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(rows[6]/1000))
        effective_end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(rows[7]/1000))
        create_at = rows[8]
        update_at = rows[9]
        print("id = %s,teacher_id = %s,weekday = %s,start_time = %s,end_time = %s,signed_id = %s,effective_start_time = %s,effective_end_time = %s,create_at =%s,update_at = %s" % \
              (id,teacher_id,weekday,start_time,end_time,signed_id,effective_start_time,effective_end_time,create_at,update_at))

except Exception as e:
    print(e)
finally:
    db.close()


