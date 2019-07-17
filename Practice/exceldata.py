# -*- coding:utf8 -*-
import xlrd


data = xlrd.open_workbook(r'D:\PycharmProjects\sishu\InterFaceTest\testData\data.xlsx')
table = data.sheets()[0]  # 选定表
nrows = table.nrows  # 选定行
# ncols = table.ncols # 选定列
# value = table.cell(1,0).value # 选定指定单元格数据

for i in range(1, nrows):  # 第0行为表头
    data = table.row_values(i)
    nation, tongue, degree, online, offline = data[0:5]
    print(nation,tongue,degree,online,offline)



