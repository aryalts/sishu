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
        code = col_code.find_one({'email': 'uat01@qq.com'}).sort("gmtCreate", -1)[0]["code"]

        # 注册帐号
        addAccount = "{\"operationName\":\"addAccount\",\"variables\":{\"input\":{\"email\":\"uat01@qq.com\",\"emailVerificationCode\":\"\",\"password\":\"111111\"}},\"query\":\"mutation addAccount($input: AddAccountInput) {\\n  addAccount(input: $input) {\\n    code\\n    teacherId\\n    token\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
        dicts_addAccount = json.loads(addAccount)
        dicts_addAccount["variables"]["input"]["emailVerificationCode"] = code
        addAccount = json.dumps(dicts_addAccount)
        addAccount_result = self.s.post(self.base_url, data=addAccount, headers=self.headers)
        dicts_addAccount_result = json.loads(addAccount_result.text)
        self.teacherId = dicts_addAccount_result['data']['addAccount']['teacherId']
        self.resumeToken = dicts_addAccount_result['data']['addAccount']['token']

    def test_01(self):
        u"""简历提交后，自动审核通过"""

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + self.resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"1\",\"phone\":\"3\",\"wechat\":\"2\"},\"isNativeSpeaker\":true,\"birthDate\":1561910400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":6},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"Basic\",\"onlineHoursPerWeek\":\"LessThanFour\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1563265330284.jpg\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1563265335147.doc\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"major\":\"2\"}],\"detailTeachingExperience\":[{\"startDate\":1561910400000,\"endDate\":1564502400000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"1\",\"jobTitle\":\"2\",\"duty\":\"3\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"pv\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"

        data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
        table = data.sheets()[0]
        data = table.row_values(1)
        nation, tongue, degree, online, offline = data[0:5]

        dicts_resumeInfoPost = json.loads(resumeInfoPost)
        dicts_resumeInfoPost["variables"]["input"]["nationality"] = nation
        dicts_resumeInfoPost["variables"]["input"]["isNativeSpeaker"] = bool(tongue)
        dicts_resumeInfoPost["variables"]["input"]["educationBackground"] = degree
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][0]["months"] = int(online)
        dicts_resumeInfoPost["variables"]["input"]["teachingExperience"][1]["months"] = int(offline)

        resumeInfoPost = json.dumps(dicts_resumeInfoPost)
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)


        # 检查老师状态
        col_teachers = self.db['teachers']
        auditStatus = col_teachers.find_one({"teacherId":self.teacherId})["auditStatus"]["status"]


        try:
            self.assertEqual(auditStatus, "None")
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


    with open('F://test//temp.html', 'wb') as fp:
    # 执行测试
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'老师注册接口测试：')
        runner.run(suite)
