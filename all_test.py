# -*- coding:utf8 -*-
import unittest
import HTMLTestRunner
import time


def all_case():
    suite = unittest.TestSuite()
    test_dir = r'D:\PycharmProjects\untitled1\testcase'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
    print(discover)
    for test_suite in discover:
        for test_case in test_suite:
            suite.addTests(test_case)
    return suite


now = time.strftime('%y-%m-%d %H-%M-%S')
filename = r'D:\PycharmProjects\untitled1\report\\' + now + 'result.html'
fp = open(filename, 'wb')
# runner = unittest.TextTestRunner()
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'私塾登录测试报告', description=u'用例执行情况')

if __name__ == '__main__':
    runner.run(all_case())
    fp.close()


