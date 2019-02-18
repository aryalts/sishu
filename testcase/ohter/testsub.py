# -*- coding:utf8 -*-

from count import Count
import unittest

class TestAdd(unittest.TestCase):

    def setUp(self):
        pass

    def test_add1(self):
        self.j = Count(2, 3)
        self.sub = self.j.add()
        self.assertEqual(self.sub, 5)

    def test_add2(self):
        self.j = Count(4.2, 2.2)
        self.sub = self.j.add()
        self.assertEqual(self.sub, 6.5)

    def test_add3(self):
        self.j = Count('lu','tishuo')
        self.sub = self.j.add()
        self.assertEquals(self.sub, 'lutishuo')

    def tearDown(self):
        pass

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(TestAdd("test_add1"))
    suite.addTest(TestAdd("test_add2"))

    runner = unittest.TextTestRunner()
    runner.run(suite)