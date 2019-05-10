# import time
#
#
# def timer(parameter): #5
#     def out_deco(func):
#         def deco():
#             if parameter == 'test1':
#                 start = time.time()
#                 time.sleep(2)
#                 func()
#                 stop = time.time()
#                 print(stop-start)
#             elif parameter == 'test2':
#                 start = time.time()
#                 time.sleep(3)
#                 func()
#                 stop = time.time()
#                 print(stop - start)
#
#         return deco
#     return out_deco
#
#
# @timer('test1')
# def test1():
#     print("test1 is running!")
#
#
# @timer('test2')
# def test2():
#     print("test2 is running!")
#
# test1() #7
# test2()


def deco(func):
    def wrapper():
        res = func()
        next(res)
        return res
    return wrapper
@deco
def foo():
    food_list = []
    while True:
        food = yield food_list
        food_list.append(food)
        print("elements in foodlist are:",food)
g = foo()
print(g.send('苹果'))
# print(g.send('香蕉'))
# print(g.send('菠萝'))
