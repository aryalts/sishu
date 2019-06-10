# -*- coding:utf8 -*-
import pymongo
import unittest
import requests
import HTMLTestRunner
import json


class CreatServiceAgreement(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://uat-svc.51uuabc.com/api/graphql'
        self.headers = {
            "authorization": "Bearer h05bPDXRUYaAuw5U1QSkwvdaq0sUmUqqPV63in2yOVI8YIirtbY2UJO_RKgTcRzys_lHUYtbKO_ILMV6YP67VQ",
            "content-type": "application/json",
            "Origin": "https://uat-teacher.51uuabc.com",
            "Referer": "https://uat-teacher.51uuabc.com/admin/teacher/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.playload = '{"operationName":"createTeacherServiceAgreement","variables":{"input":{"teacherId":"20480","signedType":"Parttime","effectiveStartTime":1559318400000,"effectiveEndTime":1561910399000,"status":"Pending","enabled":"Enabled","currency":"USD"}},"query":"mutation createTeacherServiceAgreement($input: CreateTeacherServiceAgreementInput!) {\n  createTeacherServiceAgreement(input: $input) {\n    code\n    msg\n    resultCode\n    affectedIds\n    __typename\n  }\n}\n"}'

    def test_01(self):
        u"""创建合约"""
        s = requests.session()
        r = s.post(self.base_url,data=self.playload,headers=self.headers)
        dicts = json.loads(r.text)
        print(dicts)
        self.assertEqual(dicts['data']['createTeacherServiceAgreement']['resultCode'], 'Success')

    def tearDown(self):
        client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        db = client["recruit"]
        col01 = db["serviceagreements"]
        col01.delete_one({"teacherId": "20480"})
        col02 = db["salaryagreements"]
        col02.delete_one({"teacherId": "20480"})
        col03 = db["workingtimeagreements"]
        col03.delete_one({"teacherId": "20480"})


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreatServiceAgreement('test_01'))
    # suite.addTest(Kol('test_02'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()