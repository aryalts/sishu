# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json
from public.connect_mysql_bySSH import *
import pymongo


class CreateTeacherByKol(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://uat-svc.51uuabc.com/api/graphql"
        # self.base_url = "https://qasvc.uuabc.com/api/graphql"
        self.headers = {
            'content-type': "application/json",
            # 'authorization': "Bearer qNjDK9bNC-yfPh-arO8cmu_uaTq8BoZR0iXjIh0l8bl4rVXtx46OdYjUohDKWTq1C3-PPQ3pNk10o8ku-pVoBg",
            'authorization':"Bearer 4eqd5pEHf8FdpOnc500XVE-QEAaq4p99uE3wr1wM61djXqM1RRrPAm3QYu6-sEQVC3-PPQ3pNk10o8ku-pVoBg",
            'cache-control': "no-cache",
        }
        self.s = requests.session()
        self.client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        self.db = self.client["recruit"]

    def test_01(self):
        u"""KOL创建简历"""
        addKolResume = "{\"operationName\":\"addKolResume\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"nationality\":\"United States\",\"educationBackground\":\"Bachelor\",\"isNativeSpeaker\":true,\"email\":\"uat01@qq.com\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":24},{\"name\":\"Offline\",\"months\":12}],\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1561709429805\",\"sourceType\":\"PC\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"}]}},\"query\":\"mutation addKolResume($input: AddKolResumeInput!) {\\n  addKolResume(input: $input) {\\n    code\\n    msg\\n    resumeId\\n    __typename\\n  }\\n}\\n\"}"
        addKolResume_result = self.s.post(self.base_url, data=addKolResume, headers=self.headers)

        # json字符串解码成python格式数据
        dicts_addKolResume_result = json.loads(addKolResume_result.text)

        resumeID = dicts_addKolResume_result['data']['addKolResume']['resumeId']
        # 对比返回值
        try:
            self.assertEqual(dicts_addKolResume_result['data']['addKolResume']['code'], 'OK')
        except AssertionError:
            raise
        else:
            print("KOL创建简历成功,简历ID为:{}".format(resumeID))


    def tearDown(self):
        sso_user = "select * from sso_user where email = \"uat01@qq.com\""
        uuid = connect_mysql(sso_user)[1]
        bk_user = "select * from sishu.bk_user where uuid = {} ".format(uuid)
        uid = connect_mysql(bk_user)[0]

        delete_user = 'delete from sishu.bk_user where uid ={}'.format(uid)
        connect_mysql(delete_user)
        delete_user_info = 'delete from sishu.bk_user_info where uid ={}'.format(uid)
        connect_mysql(delete_user_info)
        delete_sso_user = "delete from sso_user where sso_uuid = {}".format(uuid)
        connect_mysql(delete_sso_user)


        # client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
        # client = pymongo.MongoClient("mongodb://dds-bp1f292152f3bb54-pub.mongodb.rds.aliyuncs.com:3717/")
        # db = client["recruit"]
        # db.authenticate("qateacher","qateacher_2018",mechanism='SCRAM-SHA-1')
        col_teachers = self.db["teachers"]
        col_teachers.delete_one({'email': 'uat01@qq.com'})
        col_resumes = self.db["resumes"]
        col_resumes.delete_one({'email': 'uat01@qq.com'})
        self.client.close()


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateTeacherByKol('test_01'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()
