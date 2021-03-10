# coding:utf-8

li1 = [1, 2, 3, 4, 5]
li2 = [2, 3]

def add(num1, num2):
    print(num1+num2)
    return num1+num2

# 函数，列表１，列表２
ret = map(add, li1, li2)
print(type(ret))
print(ret)
print(list(ret))