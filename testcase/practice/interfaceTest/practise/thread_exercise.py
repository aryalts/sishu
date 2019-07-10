# -*- coding:utf8 -*-

import threading
from time import ctime,sleep


def music(fuc):
    for i in range(2):
        print("i was listing to %s %s" %(fuc,ctime()))
        sleep(7)

def movie(fuc):
     for i in range(2):
         print("i was watching to %s %s" %(fuc,ctime()))
         sleep(3)

thread = []
t1 = threading.Thread(target=music,args=(u"好运来啊",))
thread.append(t1)
t2 = threading.Thread(target=movie,args=(u"足球小将",))
thread.append(t2)

if __name__ == '__main__':
    for t in thread:
        t.setDaemon(True)
        t.start()
    for t in thread:
        t.join()
    print("i was going to bed %s" %ctime())


