# -*- coding:utf8 -*-
from selenium import webdriver
from public.login import *
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        url = "http://uat-member.51uuabc.com/wapuser/app_main.php?act=login&url="
        self.driver.get(url)
        # self.driver.implicitly_wait(10)
        locate0 = (By.ID,"username")
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located(locate0))

    def test_01(self):
        u"""登录案例参考:账号，密码正确"""
        try:
            userfile = open(r'D:\PycharmProjects\sishu\testdate\userinfo.txt', 'r')
            values = userfile.readlines()
            username = values[0].split(',')[0]
            password = values[0].split(',')[1]
            userfile.close()
            login(self.driver,username, password)

            time.sleep(5)
            locate1 = (By.XPATH, "//h4[@class='modal-title']")
            ele = WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(locate1, u'提示'))
            if ele is True:
                self.driver.find_element_by_xpath("//button[@class='btn btn-usasishu-blue btn-cancel w-100']").click()
                time.sleep(3)
                raise0 = self.driver.find_element_by_id('user-name').text
                self.assertEqual(raise0, 'uat01.test')
            else:
                raise0 = self.driver.find_element_by_id('user-name').text
                self.assertEqual(raise0, 'uat01.test')
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
            userfile = open(r'D:\PycharmProjects\sishu\testdate\userinfo.txt', 'r')
            values = userfile.readlines()
            username = values[1].split(',')[0]
            password = values[1].split(',')[1]
            userfile.close()
            login(self.driver,username, password)
            time.sleep(3)
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
            userfile = open(r'D:\PycharmProjects\sishu\testdate\userinfo.txt', 'r')
            values = userfile.readlines()
            username = values[2].split(',')[0]
            password = values[2].split(',')[1]
            userfile.close()
            login(self.driver,username, password)
            time.sleep(3)
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
    # suite.addTest(TestLogin('test_02'))
    # suite.addTest(TestLogin('test_03'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
