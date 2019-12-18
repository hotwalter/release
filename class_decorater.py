# def decorater(func):
#     print("zhuangshiqi")
#     def fn(num1,num2):
#         func(num1,num2)
#
#     return fn



# @decorater   # raw=decorater(raw)
# def raw(num1,num2):
#     print("原始函数")
#
#
#
#
# raw(1,2)

#
# def decorate(cls):
#     def wrapper():
#         print("这是类装饰器")
#     wrapper()
#     return cls
#

# def type(**kwargs):
#     def wrapper(func):
#         print(kwargs)
#
#         return func
#
#     return wrapper
#
# @type(x=1)
# class Foo:
#     pass
#
# Foo()
