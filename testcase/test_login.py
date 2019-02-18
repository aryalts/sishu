# -*- coding:utf8 -*-
from selenium import webdriver
from public.login import *
import unittest
import time


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        url = "http://uat-member.51uuabc.com/wapuser/app_main.php?act=login&url="
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def test_01(self):
        u"""登录案例参考:账号，密码正确"""
        try:
            userfile = open(r'D:\PycharmProjects\untitled1\testdate\userinfo.txt', 'r')
            values = userfile.readlines()
            username = values[0].split(',')[0]
            password = values[0].split(',')[1]
            userfile.close()
            login(self.driver,username, password)
            time.sleep(3)
            raise0 = self.driver.find_element_by_id('user-name').text
            self.assertEqual(raise0, 'uatStudent01')
        except AssertionError as msg:
            print(msg)
            raise
        else:
            print(u'正确帐号密码校验通过')
        finally:
            logout(self.driver)

    def test_02(self):
        u"""登录案例参考:账号错误"""
        try:
            userfile = open(r'D:\PycharmProjects\untitled1\testdate\userinfo.txt', 'r')
            values = userfile.readlines()
            username = values[1].split(',')[0]
            password = values[1].split(',')[1]
            userfile.close()
            login(self.driver,username, password)
            raise1 = self.driver.find_element_by_id('normal-login-error-msg').text
            self.assertEqual(raise1, u'用户不存在')
        except AssertionError as msg:
            print(msg)
            raise
        else:
            print(u'账号错误校验通过')

    def test_03(self):
        u"""登录案例参考:密码错误"""
        try:
            userfile = open(r'D:\PycharmProjects\untitled1\testdate\userinfo.txt', 'r')
            values = userfile.readlines()
            username = values[2].split(',')[0]
            password = values[2].split(',')[1]
            userfile.close()
            login(self.driver,username, password)
            raise2 = self.driver.find_element_by_id('normal-login-error-msg').text
            self.assertEqual(raise2, u'密码错误')
        except AssertionError as msg:
            print(msg)
            raise
        else:
            print(u'密码错误校验通过')

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('test_01'))
    suite.addTest(TestLogin('test_02'))
    suite.addTest(TestLogin('test_03'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
