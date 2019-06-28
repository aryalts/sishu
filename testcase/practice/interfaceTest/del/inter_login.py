# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://uat-member.51uuabc.com/api/user/user.php"

    def test_01(self):
        u"""登录密码正确"""
        self.data = {
            "username": "uat15@qq.com",
            "password": "111111",
            "device_info": "chrome 73.0.3683.103",
            "act": "login",
            "openid": "",
            "remember_me": "1",
            "device_type": "9"
        }

        s = requests.session()
        r = s.post(self.base_url, data=self.data)
        # r = requests.post(self.base_url, data=self.data)

        # json字符串解码成python格式数据
        # dicts = json.loads(r.text)
        dicts = r.json()
        print(type(dicts))
        code = r.status_code
        # 对比返回值
        self.assertEqual(code, 200)
        self.assertEqual(dicts['tips_cn'], 'SUCCESS')

    def test_02(self):
        u"""登录密码错误"""
        self.data = {
            "username": "uat15@qq.com",
            "password": "222222",
            "device_info": "chrome 73.0.3683.103",
            "act": "login",
            "openid": "",
            "remember_me": "1",
            "device_type": "9"
        }
        r = requests.post(self.base_url, self.data)
        # json字符串解码成python格式数据
        dicts = json.loads(r.text)
        code = r.status_code
        # 对比返回值
        self.assertEqual(code, 200)
        self.assertEqual(dicts['tips_cn'], u'密码错误')

    def test_03(self):
        u"""登录帐号为空"""
        self.data = {
            "username": "",
            "password": "222222",
            "device_info": "chrome 73.0.3683.103",
            "act": "login",
            "openid": "",
            "remember_me": "1",
            "device_type": "9"
        }
        r = requests.post(self.base_url, self.data)
        # json字符串解码成python格式数据
        dicts = json.loads(r.text)
        code = r.status_code
        # 对比返回值
        self.assertEqual(code, 200)
        self.assertEqual(dicts['tips'], u'账号不能为空')


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(LoginTest('test_01'))
    suite.addTest(LoginTest('test_02'))
    suite.addTest(LoginTest('test_03'))
    fp = open('F://test//temp.html', 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()
