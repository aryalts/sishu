# -*- coding:utf8 -*-
import time


# 登录
def login(driver,username, password):
    time.sleep(3)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("btn-normal-login").click()
    # driver.find_element_by_css_selector("#btn-normal-login").click()


# 退出
def logout(driver):
    # time.sleep(3)
    driver.find_element_by_id("user-name").click()
    # driver.find_element_by_id("btn-logout").click()
    # driver.find_element_by_xpath("//li[@id='btn-logout']").click()
    driver.find_element_by_css_selector("li[id='btn-logout']").click()




