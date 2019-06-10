# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json
from public.connectDB import *
import pymongo


class Kol(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://uat-svc.51uuabc.com/api/graphql"
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer qNjDK9bNC-yfPh-arO8cmu_uaTq8BoZR0iXjIh0l8bl4rVXtx46OdYjUohDKWTq1C3-PPQ3pNk10o8ku-pVoBg",
            'cache-control': "no-cache",
        }
        self.playload = "{\"operationName\":\"addKolResume\",\"variables\":{\"input\":{\"firstName\":\" First Name\",\"lastName\":\"Last Name\",\"gender\":\"Male\",\"nationality\":\"United States\",\"educationBackground\":\"Bachelor\",\"isNativeSpeaker\":true,\"email\":\"uat01@qq.com\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":24},{\"name\":\"Offline\",\"months\":12}],\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"work experience\"}]},\"curriculumVitae\":[{\"name\":\"attach2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1559715670509\",\"sourceType\":\"PC\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"},{\"key\":\"TKT\",\"value\":\"TKT\"},{\"key\":\"TEFL_TESOL_TESL\",\"value\":\"TEFL_TESOL_TESL\"},{\"key\":\"State\",\"value\":\"SEC\"},{\"key\":\"Others\",\"value\":\"O\"}]}},\"query\":\"mutation addKolResume($input: AddKolResumeInput!) {\\n  addKolResume(input: $input) {\\n    code\\n    msg\\n    resumeId\\n    __typename\\n  }\\n}\\n\"}\r\n"

    def test_01(self):
        u"""kol推荐成功"""
        s = requests.session()
        r = s.post(self.base_url, data=self.playload, headers=self.headers)
        # response = requests.request("POST", url, data=payload, headers=headers)

        # json字符串解码成python格式数据
        dicts = json.loads(r.text)
        print(dicts)
        # 对比返回值
        self.assertEqual(dicts['data']['addKolResume']['code'], 'OK')

    def test_02(self):
        u"""邮箱存在kol推荐失败"""
        s = requests.session()
        dicplayload = json.loads(self.playload)
        dicplayload['variables']['input']['email'] = 'uat45@qq.com'
        playload = json.dumps(dicplayload)

        r = s.post(self.base_url, data=playload, headers=self.headers)

        # json字符串解码成python格式数据
        dicts = json.loads(r.text)
        print(dicts)
        # 对比返回值
        self.assertEqual(dicts['data']['addKolResume']['code'], 'PERMISSION_DENY')

    def tearDown(self):
        self.sql1 = "select * from sso_user where email = 'uat01@qq.com'"
        data1 = conmysql(self.sql1)
        if data1 is not None:
            self.uuid = data1[1]
            self.sql2 = "select * from sishu.bk_user where uuid = {} ".format(self.uuid)
            data2 = conmysql(self.sql2)
            self.uid = data2[0]

            self.sql3 = 'delete from sishu.bk_user where uid ={}'.format(self.uid)
            self.sql4 = 'delete from sishu.bk_user_info where uid ={}'.format(self.uid)
            self.sql5 = "delete from sso_user where email = 'uat01@qq.com'"
            conmysql(self.sql3)
            conmysql(self.sql4)
            conmysql(self.sql5)

            myclient = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
            mydb = myclient["recruit"]
            mycol1 = mydb["teachers"]
            mycol1.delete_one({'email': 'uat01@qq.com'})
            mycol2 = mydb["resumes"]
            mycol2.delete_one({'email': 'uat01@qq.com'})

        else:
            pass


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(Kol('test_01'))
    suite.addTest(Kol('test_02'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()
