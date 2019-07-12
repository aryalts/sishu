# -*- coding:utf8 -*-
import pymongo
import unittest
import requests
import HTMLTestRunner
import json
from bsons.objectid import ObjectId


class CreatTime(unittest.TestCase):
    def setUp(self):
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
        self.playload = "{\"operationName\":\"createTeacherWorkingTimeAgreements\",\"variables\":{\"input\":{\"list\":[{\"serviceAgreementId\":\"\",\"teacherId\":\"20480\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"weekday\":\"Monday\",\"startTime\":\"09:05\",\"endTime\":\"09:35\"}]}},\"query\":\"mutation createTeacherWorkingTimeAgreements($input: CreateTeacherWorkingTimeAgreementInput!) {\\n  createTeacherWorkingTimeAgreements(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    __typename\\n  }\\n}\\n\"}"
        dicts_pload = json.loads(self.playload)
        dicts_pload["variables"]["input"]["list"][0]["serviceAgreementId"] = self._id
        self.playload = json.dumps(dicts_pload)

    def test_01(self):
        u"""创建授课时间"""
        s = requests.session()
        r = s.post(self.base_url, data=self.playload, headers=self.headers)
        self.dicts = json.loads(r.text)
        self.assertEqual(self.dicts['data']['createTeacherWorkingTimeAgreements']['resultCode'], 'Success')


    def tearDown(self):
        client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        db = client["recruit"]
        col_tm = db["workingtimeagreements"]
        self._tmid = str(col_tm.find_one({"teacherId": "20480"})['_id'])
        print(u"创建合约ID:{}的授课时间ID为:{}".format(self._id, self._tmid))
        col_tm.delete_one({"_id": ObjectId(self._tmid)})
        print(u"删除授课时间ID:{}".format(self._tmid))

        col_se = db["serviceagreements"]
        col_se.delete_one({"_id":ObjectId(self._id)})
        print(u"删除合约ID:{}".format(self._id))


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreatTime('test_01'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()