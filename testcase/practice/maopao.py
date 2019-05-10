# -*- coding:utf8 -*-
"""
#常见的冒泡排序法，如[7,2,5,1,4],一趟走完确定一个数

当 i = 0 ，进入第二个for , 循环次数5-0-1=4次，
    j = 0  [2,7,5,1,4]

    j = 1   [2,5,7,1,4]

    j = 2   [2,5,1,7,4]

    j = 3   [2,5,1,4,7]

当 i = 1 ，进入第二个for , 循环次数5-1-1=3次,
    j = 0   [2,5,1,4,7]

    j = 1   [2,1,5,4,7]

    j = 2   [2,1,4,5,7]

当 i = 2 ，进入第二个for , 循环次数5-2-1=2次,
    j = 0   [1,2,4,5,7]

    j = 1   [1,2,4,5,7]

当 i = 3 ，进入第二个for , 循环次数5-3-1=1次,
    j = 0   [1,2,4,5,7]
"""


def mp_sort(numbers):
    for i in range(len(numbers)-1):
        for j in range(len(numbers)-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers


a = [2,34,55,43,2,3,56,67,45]
print(mp_sort(a))


# 负数为真排后面，再比较两个数的绝对值，绝对值大的排后面
foo = [-5,8,0,4,9,-4,-20,-2,8,2,-4]
print(sorted(foo, key=lambda x: (x < 0, abs(x))))


# 求1~20的平方
print(list(map(lambda x: x*x, range(1, 21))))

# 求1~20之间的偶数
# 方法1
print(list(filter(lambda x: x % 2 == 0, range(1, 21))))
# 方法2 列表生成式
e = [x for x in range(1, 21) if x % 2 == 0]
print(e)

from functools import reduce
# 求1~100之和
print(reduce(lambda x, y: x+y, range(1, 5)))

# 列表每个数字加一
b = [2,34,55,43,2,3,56,67,45]
# 方法1
for i,j in enumerate(b):
    b[i] += 1
print(b)
# 方法2
print(list(map(lambda x:x+1,b)))
# 方法3
d = [i+1 for i in b]
print(d)


# 斐波那契
def fib(max):
    n,a,b = 0,0,1
    while n < max:
        a, b = b, a+b
        n += 1
        yield a


for i in  fib(5):
    print(i)