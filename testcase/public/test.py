# -*- coding:utf8 -*-
import time
print(time.localtime(time.time()))
a =time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

email = 'autotest'+a+'@qq.com'
print(email)