# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import requests
import json


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://uat-member.51uuabc.com/api/user/user.php"

    def test_login(self):
        self.data = {
            "username": "uat15@qq.com",
            "password": "111111",
            "device_info": "chrome 73.0.3683.103",
            "act": "login",
            "openid": "",
            "remember_me": "1",
            "device_type": "9",
            "af_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbmNyeXB0aW9uIjoxLCJleHAiOjE1NTgxNjMxOTMsInNzb191dWlkIjoiMjQ4ODA0NjM0MTUwMzI3MDM1In0.2TARBm9jD6BxZNBsiQPROoKeyTJ4WMmP42meFa3EQTU"
        }
        r = requests.post(self.base_url, self.data)
        # json字符串解码成python格式数据
        dicts = json.loads(r.text)
        code = r.status_code
        # 对比返回值
        self.assertEqual(code, 200)
        self.assertEqual(dicts['tips_cn'], 'SUCCESS')


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(LoginTest('test_login'))
    filename = r'D:\test\temp.html'
    fp = open(filename, 'wb')
    # 执行测试
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'接口测试用例', description=u'接口列表：')
    runner.run(suite)
    fp.close()
