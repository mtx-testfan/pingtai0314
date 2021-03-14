'''
加法运算，并发结果返回
exec(字符串的代码段，传参数(以字典的形式传递参数))

'''
content = {'data':1000}
# def test(data):
#     count = 100
#     count += data
#     return count
# result = test(content)

func = "def test(data):\n    count=100\n    count+=data\n    return count\nresult=test(data)"
exec(func,content)
# exec运行完之后，如何拿到结果->结果就存在content这个保存参数的字典中，
# 然后结果的键result，获取值content['result']
print(content['result'])
# print(content)
