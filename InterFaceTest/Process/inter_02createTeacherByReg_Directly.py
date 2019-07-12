# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json
from public.connect_mysql_bySSH import *
import pymongo
from bsons.objectid import ObjectId

class CreateTeacherByReg(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://uat-svc.51uuabc.com/api/graphql"
        self.headers = {
            'content-type': "application/json",
            'authorization':"Bearer 0LtqdRUL1W3vRhEDCHAMYiN-vp_raivu1Z3e4DMjkhPReuNG8UNGasDkQwouuWa6xTIMbQlopM6meVO9F2zvwA",
            'cache-control': "no-cache",
        }
        self.s = requests.session()
        self.client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        self.db = self.client["recruit"]


    def test_01(self):
        u"""REG创建简历"""
        # 获取注册验证码
        generateEmailVerificationCode = "{\"operationName\":\"generateEmailVerificationCode\",\"variables\":{\"input\":{\"mailTo\":\"uat01@qq.com\"}},\"query\":\"mutation generateEmailVerificationCode($input: GenerateVerificationCodeInput) {\\n  generateEmailVerificationCode(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
        self.s.post(self.base_url, data=generateEmailVerificationCode, headers=self.headers)
        col_code = self.db["verificationcodes"]
        code = col_code.find({'email': 'uat01@qq.com'}).sort("gmtCreate",-1)[0]["code"]


        # 注册帐号
        addAccount = "{\"operationName\":\"addAccount\",\"variables\":{\"input\":{\"email\":\"uat01@qq.com\",\"emailVerificationCode\":\"\",\"password\":\"111111\"}},\"query\":\"mutation addAccount($input: AddAccountInput) {\\n  addAccount(input: $input) {\\n    code\\n    teacherId\\n    token\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
        dicts_addAccount = json.loads(addAccount)
        dicts_addAccount["variables"]["input"]["emailVerificationCode"] = code
        addAccount = json.dumps(dicts_addAccount)
        addAccount_result = self.s.post(self.base_url, data=addAccount, headers=self.headers)
        dicts_addAccount_result = json.loads(addAccount_result.text)
        globals()["teacherId"] = dicts_addAccount_result['data']['addAccount']['teacherId']
        resumeToken = dicts_addAccount_result['data']['addAccount']['token']

        # 提交简历信息
        self.headers['authorization'] = "Bearer " + resumeToken
        resumeInfoPost = "{\"operationName\":\"resumeInfoPost\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"contactInfo\":{\"skype\":\"s\",\"phone\":\"p\",\"wechat\":\"w\"},\"isNativeSpeaker\":true,\"birthDate\":1559318400000,\"nationality\":\"United States\",\"currentResidence\":\"United States of America\",\"educationBackground\":\"Bachelor\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":24},{\"name\":\"Offline\",\"months\":12}],\"chineseSkill\":\"None\",\"onlineHoursPerWeek\":\"LessThanFour\",\"channelKnowUs\":\"Facebook\",\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}],\"portrait\":[{\"name\":\"timg.jpg\",\"url\":\"https://uutest2.uuabc.com/photo/1561379893272\",\"sourceType\":\"PC\"}]},\"curriculumVitae\":[{\"name\":\"2016.do\",\"url\":\"https://uutest2.uuabc.com/vitae/1561379900702\",\"sourceType\":\"PC\"}],\"academicCertificates\":[],\"teachingCertificates\":[],\"detailEducationExperience\":[{\"startDate\":1559318400000,\"endDate\":1561824000000,\"countryOfInstitution\":\"Aland Islands\",\"nameOfInstitution\":\"N\",\"major\":\"M\"}],\"detailTeachingExperience\":[{\"startDate\":1559318400000,\"endDate\":1561824000000,\"countryOfInstitution\":\"Afghanistan\",\"nameOfInstitution\":\"N\",\"jobTitle\":\"J\",\"duty\":\"D\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"}]}},\"query\":\"mutation resumeInfoPost($input: AddRegResumeInput!) {\\n  addRegResume(input: $input) {\\n    code\\n    msg\\n    __typename\\n  }\\n}\\n\"}"
        self.s.post(self.base_url, data=resumeInfoPost, headers=self.headers)


        # 检查数据库中的简历
        col_resume = self.db['resumes']
        resumeID = col_resume.find_one({"teacherId":globals()["teacherId"]})["_id"]
        fistName = col_resume.find_one({"teacherId":globals()["teacherId"]})["firstName"]

        try:
            self.assertEqual(fistName, 'uat01')
        except AssertionError:
            raise
        else:
            print("REG创建简历成功,简历ID为:{}".format(resumeID))


    def test_02(self):
        u"""面试通过"""
        updateTeacherStatus = "{\"operationName\":\"updateTeacherStatus\",\"variables\":{\"input\":{\"teacherId\":\"\",\"auditStatus\":\"InterviewPassed\",\"comments\":\"\"}},\"query\":\"mutation updateTeacherStatus($input: UpdateTeacherStatusInput) {\\n  updateTeacherStatus(input: $input) {\\n    code\\n    msg\\n    auditStatus\\n    __typename\\n  }\\n}\\n\"}"
        dicts_updateTeacherStatus = json.loads(updateTeacherStatus)

        dicts_updateTeacherStatus['variables']['input']['teacherId'] = globals()["teacherId"]
        updateTeacherStatus = json.dumps(dicts_updateTeacherStatus)
        updateTeacherStatus_result = self.s.post(self.base_url, data=updateTeacherStatus, headers=self.headers)
        dicts_updateTeacherStatus_result = json.loads(updateTeacherStatus_result.text)




        # 对比返回值
        try:
            self.assertEqual(dicts_updateTeacherStatus_result['data']['updateTeacherStatus']['code'], 'OK')
        except AssertionError:
            raise
        else:
            print("老师:{}面试通过".format(globals()["teacherId"]))

        return

    def test_03(self):
        u"""创建签约"""
        createTeacherServiceAgreement = "{\"operationName\":\"createTeacherServiceAgreement\",\"variables\":{\"input\":{\"teacherId\":\"\",\"signedType\":\"Parttime\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"status\":\"Pending\",\"enabled\":\"Enabled\",\"currency\":\"USD\"}},\"query\":\"mutation createTeacherServiceAgreement($input: CreateTeacherServiceAgreementInput!) {\\n  createTeacherServiceAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    affectedIds\\n    __typename\\n  }\\n}\\n\"}"
        dicts_createTeacherServiceAgreement = json.loads(createTeacherServiceAgreement)
        dicts_createTeacherServiceAgreement['variables']['input']['teacherId'] = globals()["teacherId"]
        createTeacherServiceAgreement = json.dumps(dicts_createTeacherServiceAgreement)
        createTeacherServiceAgreement_result = self.s.post(self.base_url, data=createTeacherServiceAgreement, headers=self.headers)
        dicts_createTeacherServiceAgreement_result = json.loads(createTeacherServiceAgreement_result.text)
        globals()["serviceAgreementId"] = dicts_createTeacherServiceAgreement_result['data']['createTeacherServiceAgreement']['affectedIds'][0]

        # 对比返回值
        try:
            self.assertEqual(dicts_createTeacherServiceAgreement_result['data']['createTeacherServiceAgreement']['resultCode'], 'Success')
        except AssertionError:
            raise
        else:
            print(u"创建合约ID为:{}".format(globals()["serviceAgreementId"]))

    def test_04(self):
        u"""创建薪资"""
        createTeacherSalaryAgreement = "{\"operationName\":\"createTeacherSalaryAgreement\",\"variables\":{\"input\":{\"serviceAgreementId\":\"\",\"teacherId\":\"\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"one2one\":0,\"smallClass\":0,\"live\":0,\"absenteeism\":0,\"openCourse\":0,\"wait\":0,\"subsidy\":0}},\"query\":\"mutation createTeacherSalaryAgreement($input: CreateTeacherSalaryAgreementInput) {\\n  createTeacherSalaryAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    affectedIds\\n    __typename\\n  }\\n}\\n\"}"
        dicts_createTeacherSalaryAgreement = json.loads(createTeacherSalaryAgreement)
        dicts_createTeacherSalaryAgreement["variables"]["input"]["serviceAgreementId"] = globals()["serviceAgreementId"]
        dicts_createTeacherSalaryAgreement["variables"]["input"]["teacherId"] = globals()["teacherId"]
        createTeacherSalaryAgreement = json.dumps(dicts_createTeacherSalaryAgreement)

        createTeacherSalaryAgreement_result = self.s.post(self.base_url, data=createTeacherSalaryAgreement, headers=self.headers)
        dicts_createTeacherSalaryAgreement_result = json.loads(createTeacherSalaryAgreement_result.text)
        globals()["salaryAgreementId"] = dicts_createTeacherSalaryAgreement_result['data']['createTeacherSalaryAgreement']['affectedIds'][0]

        # 对比返回值
        try:
            self.assertEqual(dicts_createTeacherSalaryAgreement_result['data']['createTeacherSalaryAgreement']['resultCode'], 'Success')
        except AssertionError:
            raise
        else:
            print(u"创建合约:{}的薪资ID为:{}".format(globals()["serviceAgreementId"], globals()["salaryAgreementId"]))

    def test_05(self):
        u"""创建授课时间"""
        createTeacherWorkingTimeAgreements = "{\"operationName\":\"createTeacherWorkingTimeAgreements\",\"variables\":{\"input\":{\"list\":[{\"serviceAgreementId\":\"\",\"teacherId\":\"\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"weekday\":\"Monday\",\"startTime\":\"09:05\",\"endTime\":\"09:35\"}]}},\"query\":\"mutation createTeacherWorkingTimeAgreements($input: CreateTeacherWorkingTimeAgreementInput!) {\\n  createTeacherWorkingTimeAgreements(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    __typename\\n  }\\n}\\n\"}"
        dicts_createTeacherWorkingTimeAgreements = json.loads(createTeacherWorkingTimeAgreements)
        dicts_createTeacherWorkingTimeAgreements["variables"]["input"]["list"][0]["serviceAgreementId"] = globals()["serviceAgreementId"]
        dicts_createTeacherWorkingTimeAgreements["variables"]["input"]["list"][0]["teacherId"] = globals()["teacherId"]
        createTeacherWorkingTimeAgreements = json.dumps(dicts_createTeacherWorkingTimeAgreements)

        createTeacherWorkingTimeAgreements_result = self.s.post(self.base_url, data=createTeacherWorkingTimeAgreements, headers=self.headers)
        dicts_createTeacherWorkingTimeAgreements_result = json.loads(createTeacherWorkingTimeAgreements_result.text)

        col_time = self.db["workingtimeagreements"]
        globals()["workingTimeAgreementId"] = col_time.find_one({"teacherId": globals()["teacherId"]})['_id']

        # 对比返回值
        try:
            self.assertEqual(dicts_createTeacherWorkingTimeAgreements_result['data']['createTeacherWorkingTimeAgreements']['resultCode'], 'Success')
        except AssertionError:
            raise
        else:
            print(u"创建合约:{}的授课时间ID为:{}".format(globals()["serviceAgreementId"],globals()["workingTimeAgreementId"]))



        sso_user = "select sso_uuid from sso_user where email = \"uat01@qq.com\""
        uuid = connect_mysql(sso_user)[0]
        bk_user = "select uid from sishu.bk_user where uuid = {} ".format(uuid)
        uid = connect_mysql(bk_user)[0]

        delete_user = "delete from sishu.bk_user where uid ={}".format(uid)
        connect_mysql(delete_user)
        delete_user_info = "delete from sishu.bk_user_info where uid ={}".format(uid)
        connect_mysql(delete_user_info)
        delete_sso_user = "delete from sso_user where sso_uuid ={}".format(uuid)
        connect_mysql(delete_sso_user)

        col_teachers = self.db["teachers"]
        col_teachers.delete_one({'email': 'uat01@qq.com'})
        col_resumes = self.db["resumes"]
        col_resumes.delete_one({'email': 'uat01@qq.com'})
        col_salary = self.db["salaryagreements"]
        col_salary.delete_one({"_id": ObjectId(globals()["salaryAgreementId"])})
        col_time = self.db["workingtimeagreements"]
        col_time.delete_one({"_id": globals()["workingTimeAgreementId"]})
        col_service = self.db["serviceagreements"]
        col_service.delete_one({"_id": ObjectId(globals()["serviceAgreementId"])})

        self.client.close()


    def tearDown(self):
        pass



if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateTeacherByReg('test_01'))
    suite.addTest(CreateTeacherByReg('test_02'))
    suite.addTest(CreateTeacherByReg('test_03'))
    suite.addTest(CreateTeacherByReg('test_04'))
    suite.addTest(CreateTeacherByReg('test_05'))

    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'老师注册接口测试：')
    runner.run(suite)
    fp.close()
