# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import time,os
import smtplib
from email.mime.text import MIMEText


def send_mail(file_new):
    mail_from = '875867302@qq.com'
    mail_to = 'tishuo.lu@uuabc.com'
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    msg = MIMEText(mail_body,_subtype='html',_charset='utf-8')
    msg['Subject'] = u"自动化测试报告"

    # msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    smtp.login('875867302@qq.com','lfapqstickocbdbd')
    smtp.sendmail(mail_from,mail_to,msg.as_string())
    smtp.quit()
    print('email has send out !')


def send_report(reportdir):
    lists = os.listdir(reportdir)

    lists.sort(key=lambda fn: os.path.getmtime(reportdir+"\\"+fn))
    file_new = os.path.join(reportdir,lists[-1])
    send_mail(file_new)


def creatsuite():
    testunit = unittest.TestSuite()
    test_dir = r'D:\PycharmProjects\sishu\testcase'
    discover = unittest.defaultTestLoader.discover(test_dir,pattern='test*.py',top_level_dir=None)
    for test_case in discover:
        testunit.addTests(test_case)
    return testunit


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    reportdir = 'D:\\PycharmProjects\\sishu\\report\\'
    report = reportdir + now + 'result.html'
    fp = open(report, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'自动化测试报告', description=u'用例执行情况：')
    # runner.run(creatsuite())
    fp.close()
    send_report(reportdir)










# def all_case():
#     suite = unittest.TestSuite()
#     test_dir = r'D:\PycharmProjects\sishu\testcase'
#     discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
#     for test_suite in discover:
#         for test_case in test_suite:
#             suite.addTests(test_case)
#     return suite
#
#
# now = time.strftime('%y-%m-%d %H-%M-%S')
# filename = r'D:\PycharmProjects\sishu\report\\' + now + 'result.html'
# fp = open(filename, 'wb')
# # runner = unittest.TextTestRunner()
# runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'私塾登录测试报告', description=u'用例执行情况')
#
# if __name__ == '__main__':
#     runner.run(all_case())
#     fp.close()


