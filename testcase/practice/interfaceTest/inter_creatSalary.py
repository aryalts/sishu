# -*- coding:utf8 -*-
import pymongo
import unittest
import requests
import HTMLTestRunner
import json
from bsons.objectid import ObjectId


class CreatSalary(unittest.TestCase):
    def setUp(self):
        # 取测试帐号20480的合约ID
        client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        db = client["recruit"]
        col_se = db["serviceagreements"]
        self._id = str(col_se.find_one({"teacherId": "20480"})['_id'])

        self.base_url = 'https://uat-svc.51uuabc.com/api/graphql'
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer h05bPDXRUYaAuw5U1QSkwvdaq0sUmUqqPV63in2yOVI8YIirtbY2UJO_RKgTcRzys_lHUYtbKO_ILMV6YP67VQ",
            'cache-control': "no-cache",
        }
        self.playload = "{\"operationName\":\"createTeacherSalaryAgreement\",\"variables\":{\"input\":{\"serviceAgreementId\":\"\",\"teacherId\":\"20480\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"one2one\":0,\"smallClass\":0,\"live\":0,\"absenteeism\":0,\"openCourse\":0,\"wait\":0,\"subsidy\":0}},\"query\":\"mutation createTeacherSalaryAgreement($input: CreateTeacherSalaryAgreementInput) {\\n  createTeacherSalaryAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    __typename\\n  }\\n}\\n\"}"
        dicts_pload = json.loads(self.playload)
        dicts_pload["variables"]["input"]["serviceAgreementId"] = self._id
        print(dicts_pload)
        self.playload = dicts_pload
        print(self.playload)

    def test_01(self):
        u"""创建薪资"""
        s = requests.session()
        r = s.post(self.base_url, data=self.playload, headers=self.headers)
        dicts = json.loads(r.text)
        self.assertEqual(dicts['data']['createTeacherSalaryAgreement']['resultCode'], 'Success')

    # def tearDown(self):
    #     # client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
    #     # db = client["recruit"]
    #     # col_sa = db["salaryagreements"]
    #     # col_sa.delete_one({"_id": ObjectId("5d033ece5276f8243daa2af4")})


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreatSalary('test_01'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()