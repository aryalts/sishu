# -*- coding:utf8 -*-
from selenium import webdriver
import unittest
from selenium.webdriver.support import expected_conditions as EC
import time


class AddReferral(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        url = "http://uat-member.51uuabc.com/wapuser/app_main.php?act=login&url="
        self.driver.get(url)
        # 通过cookie直接登录
        self.driver.add_cookie({'name':'PHPSESSID','value':'dc49gc45u9oj99cksmss6ntd80'})
        self.driver.refresh()

    def test_01(self):
        u"""增加推荐人案例参考:正常提交"""
        try:
            time.sleep(10)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/ul/li[7]/div').click()
            time.sleep(1)
            self.driver.switch_to.frame("open-live-room-iframe")
            time.sleep(1)
            self.driver.find_element_by_xpath("//*[@id='Myreferrals']/div/div[1]/div[1]/div[3]/a").click()
            time.sleep(1)
            a = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/input").send_keys(a)
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/input").send_keys("test")
            time.sleep(1)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div:nth-child(4) > div > div > input").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(1)").click()
            time.sleep(1)
            email = 'autotest'+a+'@qq.com'
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div:nth-child(5) > input").send_keys(email)
            time.sleep(1)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div:nth-child(6) > input").send_keys(email)
            time.sleep(1)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div:nth-child(7) > div > div.el-input.el-input--suffix > input").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("body > div:nth-child(6) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(1) > span").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div:nth-child(8) > div > div > input").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("body > div:nth-child(7) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(1)").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div:nth-child(9) > div > div.el-input.el-input--suffix > input").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("body > div:nth-child(8) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(3) > span").click()
            time.sleep(1)

            # self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div.inputdiv > div > div.teaching_t > div:nth-child(1) > div.el-input.el-input--suffix > input").click()
            # self.driver.find_element_by_css_selector("body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(4)").click()
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_left > div > div.inputdiv2 > div > div:nth-child(3) > label > span.el-radio__input > span").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.cont_right > div > div.inputDiv > div > textarea").send_keys("good teacher")
            time.sleep(1)
            self.driver.find_element_by_css_selector("#Vitae").send_keys(r'D:\\BugReport.txt')
            time.sleep(2)
            self.driver.find_element_by_css_selector("#warm > div > div.cont > div.button_all > button").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("#resumeCollectInfo > div.showHome > div > div > div > span.btn.btn_next").click()
            time.sleep(1)
            raise0 = self.driver.find_element_by_xpath("//*[@id='Myreferrals']/div/div[1]/div[1]/div[1]/span").text
            time.sleep(3)
            self.assertEqual(raise0,'1njck0')
        except AssertionError as msg:
            print(msg)
            raise
        else:
            print(u'推荐人增加成功')

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(AddReferral('test_01'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
