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
            'content-type': "application/json",
            'authorization': "Bearer h05bPDXRUYaAuw5U1QSkwvdaq0sUmUqqPV63in2yOVI8YIirtbY2UJO_RKgTcRzys_lHUYtbKO_ILMV6YP67VQ",
            'cache-control': "no-cache",
        }
        self.playload = "{\"operationName\":\"createTeacherSalaryAgreement\",\"variables\":{\"input\":{\"serviceAgreementId\":\"5cfe3737fc90a45ac9ae15ca\",\"teacherId\":\"20480\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"one2one\":0,\"smallClass\":0,\"live\":0,\"absenteeism\":0,\"openCourse\":0,\"wait\":0,\"subsidy\":0}},\"query\":\"mutation createTeacherSalaryAgreement($input: CreateTeacherSalaryAgreementInput) {\\n  createTeacherSalaryAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    __typename\\n  }\\n}\\n\"}"

    def test_01(self):
        u"""创建薪资"""
        s = requests.session()
        r = s.post(self.base_url, data=self.playload, headers=self.headers)
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