# -*- coding:utf8 -*-
import pymongo
import requests
import json
from bsons.objectid import ObjectId


def addTeacher(email_demo,fname,lname):
    base_url = 'https://uat-svc.51uuabc.com/api/graphql'
    headers = {
        "authorization": "Bearer h05bPDXRUYaAuw5U1QSkwvdaq0sUmUqqPV63in2yOVI8YIirtbY2UJO_RKgTcRzys_lHUYtbKO_ILMV6YP67VQ",
        "content-type": "application/json",
        "Origin": "https://uat-teacher.51uuabc.com",
        "Referer": "https://uat-teacher.51uuabc.com/admin/teacher/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    # 创建账号
    s = requests.session()
    p4 = "{\"operationName\":\"addAccount\",\"variables\":{\"input\":{\"email\":\"\",\"byAdmin\":true}},\"query\":\"mutation addAccount($input: AddAccountInput) {\\n  addAccount(input: $input) {\\n    teacherId\\n    ssoUuid\\n    token\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
    dicts_p4 = json.loads(p4)
    dicts_p4["variables"]["input"]["email"] = email_demo
    p4 = json.dumps(dicts_p4)
    r4 = s.post(base_url,data=p4,headers=headers)
    dicts4 = json.loads(r4.text)
    teacherId = dicts4['data']['addAccount']['teacherId']
    print(u"创建老师ID为:{}".format(teacherId))

    # 老师信息
    p5 = "{\"operationName\":\"updateTeacher\",\"variables\":{\"input\":{\"teacherId\":\"\",\"firstName\":\"\",\"lastName\":\"\",\"gender\":\"Male\",\"birthDate\":1559318400000,\"contactInfo\":{\"skype\":\"s\",\"wechat\":\"w\",\"phone\":\"p\"},\"isNativeSpeaker\":true,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"detailEducationExperience\":[{\"startDate\":\"2019-05-31T16:00:00.000Z\",\"endDate\":\"2019-06-29T16:00:00.000Z\",\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"N\",\"major\":\"M\"}],\"teachingExperience\":[{\"name\":\"Online\",\"months\":24},{\"name\":\"Offline\",\"months\":12}],\"detailTeachingExperience\":[{\"startDate\":\"2019-05-31T16:00:00.000Z\",\"endDate\":\"2019-06-29T16:00:00.000Z\",\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"N\",\"jobTitle\":\"J\",\"duty\":\"D\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"}],\"chineseSkill\":\"None\",\"onlineHoursPerWeek\":\"LessThanFour\",\"channelKnowUs\":\"Facebook\",\"refererDetail\":{\"referenceCode\":\"\",\"referenceTeacherId\":\"\"},\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"CN\",\"text\":\"中文自我介绍\"},{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"英文自我介绍\"}],\"portrait\":[{\"name\":\"small\",\"url\":\"https://uutest2.uuabc.com/teacher/passport/201951910847/uploadPassport\",\"desc\":\"teacherAdminCreat\",\"sourceType\":\"PC\"}],\"video\":[{\"name\":\"forStudent\",\"url\":\"https://uutest2.uuabc.com/teacher/video/2019519101052/1.mp4\",\"desc\":\"teacherAdminCreat\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":{\"name\":\"\",\"url\":\"\",\"desc\":\"teacherAdminCreat\",\"sourceType\":\"PC\"},\"academicCertificates\":[],\"teachingCertificates\":[],\"emergencyContact\":{\"name\":\"\",\"phone\":\"\"},\"comments\":\"\",\"entryDate\":1559318400000,\"firstPageOfPassport\":{\"name\":\"passport\",\"url\":\"\",\"desc\":\"teacherAdminCreat\",\"sourceType\":\"PC\"},\"passportId\":\"\",\"schoolInService\":\"北京大学\",\"beGoodAtTeachingTypes\":[\"1|146|147\",\"1|146|148\",\"1|146|149\",\"1|146|150\",\"1|146|151\",\"1|146|954\",\"1|500|563\",\"1|501|507\",\"1|501|508\",\"1|924|925\"],\"level\":1}},\"query\":\"mutation updateTeacher($input: UpdateTeacherInput) {\\n  updateTeacher(input: $input) {\\n    code\\n    msg\\n    teacher {\\n      id\\n      uuid\\n      teacherId\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"
    dicts_p5 = json.loads(p5)
    dicts_p5["variables"]["input"]["teacherId"] = teacherId
    dicts_p5["variables"]["input"]["firstName"] = fname
    dicts_p5["variables"]["input"]["lastName"] = lname
    p5 = json.dumps(dicts_p5)
    r5 = s.post(base_url,data=p5,headers=headers)
    dicts5 = json.loads(r5.text)
    result5 = dicts5['data']['updateTeacher']['code']
    print(u"老师信息保存结果为:{}".format(result5))

    # 更新老师状态
    p6 = "{\"operationName\":\"updateTeacherStatus\",\"variables\":{\"input\":{\"teacherId\":\"\",\"auditStatus\":\"TrainingFinished\",\"comments\":\"\"}},\"query\":\"mutation updateTeacherStatus($input: UpdateTeacherStatusInput) {\\n  updateTeacherStatus(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
    dicts_p6 = json.loads(p6)
    dicts_p6["variables"]["input"]["teacherId"] = teacherId
    p6 = json.dumps(dicts_p6)
    r6 = s.post(base_url,data=p6,headers=headers)
    dicts6 = json.loads(r6.text)
    result6 = dicts6['data']['updateTeacherStatus']['code']
    print(u"老师状态更新结果为:{}".format(result6))

    # 创建合约
    p1 = "{\"operationName\":\"createTeacherServiceAgreement\",\"variables\":{\"input\":{\"teacherId\":\"\",\"signedType\":\"Parttime\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"status\":\"Pending\",\"enabled\":\"Enabled\",\"currency\":\"USD\"}},\"query\":\"mutation createTeacherServiceAgreement($input: CreateTeacherServiceAgreementInput!) {\\n  createTeacherServiceAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    affectedIds\\n    __typename\\n  }\\n}\\n\"}"
    dicts_p1 = json.loads(p1)
    dicts_p1["variables"]["input"]["teacherId"] = teacherId
    p1 = json.dumps(dicts_p1)
    r1 = s.post(base_url,data=p1,headers=headers)
    dicts1 = json.loads(r1.text)
    _id = dicts1['data']['createTeacherServiceAgreement']['affectedIds'][0]
    print(u"创建合约ID为:{}".format(_id))

    # "修改签约状态
    client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
    db = client["recruit"]
    col_se = db["serviceagreements"]
    myquery = {"_id" : ObjectId(_id)}
    newvalues = {"$set": {"status" : 1}}
    col_se.update_one(myquery, newvalues)

    # "创建薪资"
    p2 = "{\"operationName\":\"createTeacherSalaryAgreement\",\"variables\":{\"input\":{\"serviceAgreementId\":\"\",\"teacherId\":\"\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"one2one\":0,\"smallClass\":0,\"live\":0,\"absenteeism\":0,\"openCourse\":0,\"wait\":0,\"subsidy\":0}},\"query\":\"mutation createTeacherSalaryAgreement($input: CreateTeacherSalaryAgreementInput) {\\n  createTeacherSalaryAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    affectedIds\\n    __typename\\n  }\\n}\\n\"}"
    dicts_p2 = json.loads(p2)
    dicts_p2["variables"]["input"]["serviceAgreementId"] = _id
    dicts_p2["variables"]["input"]["teacherId"] = teacherId
    p2 = json.dumps(dicts_p2)
    r2 = s.post(base_url, data=p2, headers=headers)
    dicts2 = json.loads(r2.text)
    _said = dicts2['data']['createTeacherSalaryAgreement']['affectedIds'][0]
    print(u"创建合约ID:{}的薪资ID:{}".format(_id, _said))

    # "创建授课时间"
    p3 = "{\"operationName\":\"createTeacherWorkingTimeAgreements\",\"variables\":{\"input\":{\"list\":[{\"serviceAgreementId\":\"\",\"teacherId\":\"\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"weekday\":\"Monday\",\"startTime\":\"09:05\",\"endTime\":\"09:35\"}]}},\"query\":\"mutation createTeacherWorkingTimeAgreements($input: CreateTeacherWorkingTimeAgreementInput!) {\\n  createTeacherWorkingTimeAgreements(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    __typename\\n  }\\n}\\n\"}"
    dicts_p3 = json.loads(p3)
    dicts_p3["variables"]["input"]["list"][0]["serviceAgreementId"] = _id
    dicts_p3["variables"]["input"]["list"][0]["teacherId"] = teacherId
    p3 = json.dumps(dicts_p3)
    s.post(base_url, data=p3, headers=headers)
    col_tm = db["workingtimeagreements"]
    _tmid = str(col_tm.find_one({"teacherId": teacherId})['_id'])
    col_tm.find_one({"_id": ObjectId(_tmid)})
    print(u"创建合约ID:{}的授课时间ID:{}".format(_id, _tmid))



addTeacher(email_demo="uat016@qq.com",fname="uat016",lname="test")

