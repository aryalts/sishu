# -*- coding:utf8 -*-

from selenium import webdriver
import unittest
import time


class TestAddTeacher(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        url = "https://uat-teacher.51uuabc.com/admin/teacher/#/createTeacher?token=taIFjGPTGqiJXGgyruN69__T2zrkQDAd1GjPWo-FblwwGmuWcTWPcP7ggODgq9uEjaCod4Kf3tSZQblf9VK-JA"
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def test_01(self):
        u"""创建账号，邮箱未使用过"""
        # 登录邮箱
        file = open(r'D:\PycharmProjects\sishu\testdate\email.txt','r')
        content = file.readlines()
        email = content[0]
        file.close()
        self.driver.find_element_by_xpath("//input[@class='el-input__inner'and@class='el-input__inner']").send_keys(email)
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[1]/div[3]/button[2]/span").click()
        time.sleep(1)
        # 渠道
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[1]/div[2]/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/ul/li[4]/span").click()
        # 推荐人
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[2]/div[2]/div/label[2]/span[1]/span").click()
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[3]/div[2]/div/input").send_keys(20001)
        # 入职日期
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[5]/div[2]/div/input").send_keys("2018-12-01")
        # 老师等级
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[6]/div[2]/div/div[1]/input").click()
        self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[1]/ul/li[6]/span").click()
        # 可教类型
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[7]/div[2]/div/div[1]/div/label/span/span").click()
        # 老师头像
        self.driver.find_element_by_xpath("//*[@id='uploadPassport']").send_keys(r'D:\PycharmProjects\sishu\testcase\attach\1.PNG')
        time.sleep(5)
        # FirstName
        name = email.split('@')[0]
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[9]/div[2]/div/input").send_keys(name)
        # LastName
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[10]/div[2]/div/input").send_keys("test")
        # 性别
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[11]/div[2]/div/div/input").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/ul/li[1]/span").click()
        # 生日
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[12]/div[2]/div/input").send_keys("2010-04-01")
        # 国籍
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[14]/div[2]/div/div[1]/label[1]/span[1]/span").click()
        # 现居地
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[15]/div[2]/div/div[2]/label[2]/span[1]/span").click()
        # 手机号码
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[16]/div[2]/div/input").send_keys(138189101690)
        # 微信
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[17]/div[2]/div/input").send_keys("weixin")
        # skype
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[18]/div[2]/div/input").send_keys("sarahjanehiggs")
        # 紧急联系人
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[19]/div[2]/div/input").send_keys(u"联系人张三")
        # 紧急联系人电话
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[20]/div[2]/div/input").send_keys(13818901600)
        # 最高学历：博士
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[21]/div[2]/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[1]/ul/li[3]/span").click()
        # 英语母语
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[23]/div[2]/div/div[1]/input").click()
        self.driver.find_element_by_xpath("/html/body/div[8]/div[1]/div[1]/ul/li[1]/span").click()
        # 中文水平基础
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[24]/div[2]/div/div[1]/input").click()
        self.driver.find_element_by_xpath("/html/body/div[9]/div[1]/div[1]/ul/li[2]/span").click()
        # 每周上课时间
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[25]/div[2]/div/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[10]/div[1]/div[1]/ul/li[2]/span").click()
        # 教学经验
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[26]/div[2]/div/div[1]/div[1]/div[1]/input").click()
        self.driver.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/ul/li[4]/span").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[26]/div[2]/div/div[2]/div[1]/div/input").click()
        self.driver.find_element_by_xpath("/html/body/div[12]/div[1]/div[1]/ul/li[3]/span").click()
        # 任职学校
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[27]/div[2]/div[1]/label/span[1]/span").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[27]/div[2]/div[1]/div/input").send_keys(u"北京大学")
        # 教学证书
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[28]/div[2]/div[1]/label/span[1]/span").click()
        self.driver.find_element_by_xpath("//*[@id='baseInfo']/div[2]/div[28]/div[2]/div[1]/div/div[1]/label[1]/span[1]/span").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[28]/div[2]/div[1]/div/div[3]/label/span[1]/span").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[28]/div[2]/div[1]/div/div[3]/div/input").send_keys(u"软件评测师")
        # 教学证书附件
        self.driver.find_element_by_xpath("//*[@id='Upctf']").send_keys(r"D:\PycharmProjects\sishu\testcase\attach\1.png")
        # 简历
        self.driver.find_element_by_xpath("//*[@id='Vitae']").send_keys(r"D:\PycharmProjects\sishu\testcase\attach\1.png")
        # 自我介绍
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[31]/div[2]/div/textarea").send_keys(u"嗨，我叫迈克，自2009年以来，我一直在教4到70岁不等的学生ESL。我来自新泽西，目前和家人住在西班牙。我真的很喜欢教英语，我相信无论你的水平如何，我都能提高你的英语水平。在空闲时间，我喜欢和家人一起读书、打篮球和摄影。")
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[32]/div[2]/div/textarea").send_keys("Hi, my name is Mike, and I have been teaching ESL to students varying in ages from 4 to 70 since 2009.  I am from New Jersey, and currently live in Spain with my family.  I really enjoy teaching English, and I am confident that I can improve your English, no matter your level. In my free time, I enjoy spending time with my family, reading, playing basketball and photography.")
        # 自我介绍视频
        self.driver.find_element_by_xpath("//*[@id='uploadVideo']").send_keys(r"D:\PycharmProjects\sishu\testcase\attach\1.mp4")
        # 护照
        self.driver.find_element_by_xpath("//*[@id='uploadPhoto']").send_keys(r"D:\PycharmProjects\sishu\testcase\attach\1.png")
        # 支付方式
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[35]/div[2]/div/label[1]/span[1]/span").click()
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[36]/div[2]/div[1]/input").send_keys("Stewart Johnston")
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[36]/div[2]/div[2]/input").send_keys("kalmproducts@gmail.com")
        # 备注
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[38]/div[2]/div/textarea").send_keys(u"备注")


        # self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/button").click()


    # def tearDown(self):
    #     self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestAddTeacher(test_01))

    runner = unittest.TextTestRunner()
    runner.run(suite)