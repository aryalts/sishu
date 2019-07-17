import pymongo

client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
db = client["recruit"]
col_teachers = db['teachers']
auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]
print(auditStatus)
print(col_teachers.find_one({"email" : "uat01@qq.com"}))






