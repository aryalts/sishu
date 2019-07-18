# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json
import sys
sys.path.append(r"D:\PycharmProjects\sishu\InterFaceTest\testCase\function\public\\")
from connect_mysql_bySSH import *
import pymongo
import xlrd
import time

class CreateTeacherByReg(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://uat-svc.51uuabc.com/api/graphql"
        self.headers = {
            'content-type': "application/json",
            'authorization':"Bearer 0LtqdRUL1W3vRhEDCHAMYiN-vp_raivu1Z3e4DMjkhPReuNG8UNGasDkQwouuWa6xTIMbQlopM6meVO9F2zvwA",
            'cache-control': "no-cache",
        }


        # 获取注册验证码
        self.s = requests.session()
        self.client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        self.db = self.client["recruit"]
        generateEmailVerificationCode = "{\"operationName\":\"generateEmailVerificationCode\",\"variables\":{\"input\":{\"mailTo\":\"uat01@qq.com\"}},\"query\":\"mutation generateEmailVerificationCode($input: GenerateVerificationCodeInput) {\\n  generateEmailVerificationCode(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
        self.s.post(self.base_url, data=generateEmailVerificationCode, headers=self.headers)
        col_code = self.db["verificationcodes"]
        code = col_code.find({'email': 'uat01@qq.com'}).sort("gmtCreate", -1)[0]["code"]



        # 注册帐号
        addAccount = "{\"operationName\":\"addAccount\",\"variables\":{\"input\":{\"email\":\"uat01@qq.com\",\"emailVerificationCode\":\"\",\"password\":\"111111\"}},\"query\":\"mutation addAccount($input: AddAccountInput) {\\n  addAccount(input: $input) {\\n    code\\n    teacherId\\n    token\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
        dicts_addAccount = json.loads(addAccount)
        dicts_addAccount["variables"]["input"]["emailVerificationCode"] = code

        addAccount = json.dumps(dicts_addAccount)

        addAccount_result = self.s.post(self.base_url, data=addAccount, headers=self.headers)

        print(addAccount_result)
        dicts_addAccount_result = json.loads(addAccount_result.text)

        print(dicts_addAccount_result)
        self.teacherId = dicts_addAccount_result['data']['addAccount']['teacherId']
        self.resumeToken = dicts_addAccount_result['data']['addAccount']['token']
        print(self.resumeToken)


    def test_01(self):
        u"""简历提交后，自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(1)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))

    def test_02(self):
        u"""非优选国籍，不会自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(2)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))

    def test_03(self):
        u"""非英语母语，不会自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(3)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))


    def test_04(self):
        u"""非本科以上学历，不会自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(4)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))

    def test_05(self):
        u"""线上工作经验满足12个月，自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(5)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))

    def test_06(self):
        u"""线下工作经验满足12个月，自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(6)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))


    def test_07(self):
        u"""线上工作经验不满12个月，不会自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(7)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))


    def test_08(self):
        u"""线下工作经验不满12个月，不会自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(8)
        nation, tongue, degree, online, offline ,status= data[0:6]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)
        time.sleep(3)

        # 执行定时任务
        base_url = "http://uat-svc.51uuabc.com:14495/api/handler/autoSetResumePass"
        self.s.post(base_url,data="",headers=self.headers)

        time.sleep(1)
        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"email" : "uat01@qq.com"})["auditStatus"]["status"]

        try:
            self.assertEqual(auditStatus, status)
        except AssertionError:
            raise
        else:
            print("简历状态更新为:{}".format(auditStatus))



    def tearDown(self):
        delSql = "DELETE a,b,c from sso_user a LEFT JOIN sishu.bk_user b on (a.sso_uuid = b.uuid) LEFT JOIN sishu.bk_user_info c on b.uid = c.uid where a.email= 'uat01@qq.com'"
        connect_mysql(delSql)


        col_teachers = self.db["teachers"]
        col_teachers.delete_one({'email': 'uat01@qq.com'})
        col_resumes = self.db["resumes"]
        col_resumes.delete_one({'email': 'uat01@qq.com'})


        self.client.close()


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateTeacherByReg('test_01'))
    suite.addTest(CreateTeacherByReg('test_02'))
    suite.addTest(CreateTeacherByReg('test_03'))
    suite.addTest(CreateTeacherByReg('test_04'))
    suite.addTest(CreateTeacherByReg('test_05'))
    suite.addTest(CreateTeacherByReg('test_06'))
    suite.addTest(CreateTeacherByReg('test_07'))
    suite.addTest(CreateTeacherByReg('test_08'))


    with open('F://test//temp.html', 'wb') as fp:
    # 执行测试
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'老师注册接口测试：')
        runner.run(suite)
