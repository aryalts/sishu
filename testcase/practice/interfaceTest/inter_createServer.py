# -*- coding:utf8 -*-
import pymongo
import unittest
import requests
import HTMLTestRunner
import json
from bsons.objectid import ObjectId

"""下载PyMongo模块时 它会有一个相对应bson模块 也就是说 PyMongo模块的实现是基于和它一起的bson模块的 
该bson模块 并非我们用 pip install bson 安装的 bson。 
当你的系统环境下 同时具备这两个模块时 PyMongo模块和bson模块的相对应功能便会挂掉 .
解决方案：在需要bson模块时 将其下载好 放置自己项目的目录下 并改名使用
原文：https://blog.csdn.net/weixin_39352438/article/details/80109647 
"""


class CreatService(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://uat-svc.51uuabc.com/api/graphql'
        self.headers = {
            "authorization": "Bearer h05bPDXRUYaAuw5U1QSkwvdaq0sUmUqqPV63in2yOVI8YIirtbY2UJO_RKgTcRzys_lHUYtbKO_ILMV6YP67VQ",
            "content-type": "application/json",
            "Origin": "https://uat-teacher.51uuabc.com",
            "Referer": "https://uat-teacher.51uuabc.com/admin/teacher/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.playload = "{\"operationName\":\"createTeacherServiceAgreement\",\"variables\":{\"input\":{\"teacherId\":\"20480\",\"signedType\":\"Parttime\",\"effectiveStartTime\":1559318400000,\"effectiveEndTime\":1561910399000,\"status\":\"Pending\",\"enabled\":\"Enabled\",\"currency\":\"USD\"}},\"query\":\"mutation createTeacherServiceAgreement($input: CreateTeacherServiceAgreementInput!) {\\n  createTeacherServiceAgreement(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    affectedIds\\n    __typename\\n  }\\n}\\n\"}"

    def test_01(self):
        u"""创建合约"""
        s = requests.session()
        r = s.post(self.base_url,data=self.playload,headers=self.headers)
        self.dicts = json.loads(r.text)
        self.assertEqual(self.dicts['data']['createTeacherServiceAgreement']['resultCode'], 'Success')

    def tearDown(self):
        self._id = self.dicts['data']['createTeacherServiceAgreement']['affectedIds'][0]
        print(u"创建合约ID为:{}".format(self._id))


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreatService('test_01'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()