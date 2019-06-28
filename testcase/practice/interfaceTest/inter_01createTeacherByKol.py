# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json
from public.connect_mysql_bySSH import *
import pymongo


class CreateResumeByKol(unittest.TestCase):
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


    def test_01(self):
        u"""KOL创建简历"""
        addKolResume = "{\"operationName\":\"addKolResume\",\"variables\":{\"input\":{\"firstName\":\"uat01\",\"lastName\":\"test\",\"gender\":\"Male\",\"nationality\":\"United States\",\"educationBackground\":\"Bachelor\",\"isNativeSpeaker\":true,\"email\":\"uat01@qq.com\",\"teachingExperience\":[{\"name\":\"Online\",\"months\":24},{\"name\":\"Offline\",\"months\":12}],\"selfIntroduction\":{\"text\":[{\"name\":\"short\",\"lang\":\"EN\",\"text\":\"123\"}]},\"curriculumVitae\":[{\"name\":\"2016.doc\",\"url\":\"https://uutest2.uuabc.com/vitae/1561709429805\",\"sourceType\":\"PC\"}],\"teachingCertificateTypes\":[{\"key\":\"CELTA\",\"value\":\"CELTA\"}]}},\"query\":\"mutation addKolResume($input: AddKolResumeInput!) {\\n  addKolResume(input: $input) {\\n    code\\n    msg\\n    resumeId\\n    __typename\\n  }\\n}\\n\"}"
        addKolResume_result = self.s.post(self.base_url, data=addKolResume, headers=self.headers)
        # json字符串解码成python格式数据
        dicts_addKolResume_result = json.loads(addKolResume_result.text)
        # 对比返回值
        try:
            self.assertEqual(dicts_addKolResume_result['data']['addKolResume']['code'], 'OK')
        except AssertionError:
            raise
        else:
            print("KOL创建老师简历成功")


    def tearDown(self):
        self.select_sso_user = "select * from sso_user where email = \"uat01@qq.com\""
        sso_data = connect_mysql(self.select_sso_user)
        print(sso_data)
        if sso_data is not None:
            self.uuid = sso_data[1]
            self.select_user_data = "select * from sishu.bk_user where uuid = {} ".format(self.uuid)
            user_data = connect_mysql(self.select_user_data)
            self.uid = user_data[0]
            self.delete_user_data = 'delete from sishu.bk_user where uid ={}'.format(self.uid)
            connect_mysql(self.delete_user_data)
            self.delete_user_info = 'delete from sishu.bk_user_info where uid ={}'.format(self.uid)
            connect_mysql(self.delete_user_info)
            self.delete_sso_user = "delete from sso_user where email = 'uat01@qq.com'"
            connect_mysql(self.delete_sso_user)


            client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
            # client = pymongo.MongoClient("mongodb://dds-bp1f292152f3bb54-pub.mongodb.rds.aliyuncs.com:3717/")
            db = client["recruit"]
            # db.authenticate("qateacher","qateacher_2018",mechanism='SCRAM-SHA-1')
            col_teachers = db["teachers"]
            col_teachers.delete_one({'email': 'uat01@qq.com'})
            col_resumes = db["resumes"]
            col_resumes.delete_one({'email': 'uat01@qq.com'})
            client.close()

        else:
            pass


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateTeacherByKol('test_01'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()
