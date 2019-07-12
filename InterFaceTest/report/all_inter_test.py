# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import time,os
import smtplib
from email.mime.text import MIMEText # 发送正文
from email.mime.multipart import MIMEMultipart # 发送多个部分
from email.mime.application import MIMEApplication # 发送附件


def send_mail(file_new):
    sender = 'lutishuo@126.com'
    receiver = ['tishuo.lu@uuabc.com','875867302@qq.com']

    # f = open(file_new, 'rb')
    # mail_body = f.read()
    # f.close()
    with open(file_new, 'rb') as f:
        mail_body = f.read()

    msg = MIMEMultipart()
    part1 = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg.attach(part1)

    part2 = MIMEApplication(mail_body)
    part2.add_header('Content-Disposition','attachment',filename='file.html')
    msg.attach(part2)

    msg['Subject'] = u"自动化测试报告"
    msg['from'] = 'lutishuo@126.com'
    msg['to'] = ','.join(receiver)


    smtp = smtplib.SMTP()
    smtp.connect('smtp.126.com')
    smtp.login('lutishuo@126.com','lts103613')
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()
    print('email has send out !')


def send_report(report_dir):
    lists = os.listdir(report_dir)
    # sort按key的关键字进行排序，lambda的入参x为lists列表的元素，获取文件的最后修改时间，x只是临时起的一个名字，你可以使用任意的名字；
    lists.sort(key=lambda x: os.path.getmtime(report_dir+"\\"+x))
    file_new = os.path.join(report_dir,lists[-1])
    send_mail(file_new)


def creat_suite():
    test_unit = unittest.TestSuite()
    test_dir = r'D:\PycharmProjects\sishu\InterFaceTest\testCase\process\\'
    discover = unittest.defaultTestLoader.discover(test_dir,pattern='inter_0*.py',top_level_dir=None)
    for test_case in discover:
        test_unit.addTests(test_case)
    return test_unit


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    report_dir = r'D:\PycharmProjects\sishu\InterFaceTest\report\\'
    report = report_dir + now + ' ' + 'report.html'
    fp = open(report, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'自动化测试报告', description=u'用例执行情况：')
    runner.run(creat_suite())
    fp.close()
    send_report(report_dir)










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


