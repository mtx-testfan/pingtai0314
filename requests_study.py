'''
python做接口自动化测试
requests库
get  关键字参数params(构造成字典)
post
1.表单(k=v&k=v)   关键字参数 data(构造成字典)
2.json            关键字参数 json(json数据原封不动)
-----------
响应的方法
resp.text   返回字符串的数据类型--对resp的数据结构没有限制，响应值是字符串，是json的，都可以解析
resp.json()   返回的是字典的数据类型--resp是json的数据{}，没有办法对字符串进行解析
'''
# 一.get请求
import requests
ip = 'http://localhost:8080/'
# url = ip + '/pinter/com/getSku'
# # 以字典的形式进行传递
# param = {'id':1}
# # response = requests.get(url,params=param)
# #改写
# response = requests.request('get',url,params=param)
# print('响应值是',response)
# res_text = response.text # 数据类型是字符串的
# print('响应值res_text的值是{}，数据类型是{}'.format(res_text,type(res_text)))
# res_json = response.json()  # 返回的数据类型是字典
# print('响应的值res_json的值是{}，数据类型是{}'.format(res_json,type(res_json)))
# #响应的作用：1.断言assert 2.数据提取extract
# 二.post请求
# 2.1 请求参数是form表单的形式--请求体的关键字data=变量
# url = ip + '/pinter/com/login'
# # 以字典的形式进行传递
# data = {
#     "userName":'admin',
#     "password":'123456'
# }
# # resp = requests.post(url, data=data)
# # 改写
# resp=requests.request('post',url,data=data)
# print(resp.json())
# 2.2 请求参数是json的形式---请求体的关键字json=变量
url = ip + "/pinter/com/register"
json = {"userName":"test","password":"1234","gender":1,"phoneNum":"110","email":"beihe@163.com","address":"Beijing"}
# resp = requests.post(url,json=json)
# 改写
resp =requests.request('post',url,json=json)
print(resp.json())
message = resp.json().get('message')
print(message)