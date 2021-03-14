'''
逻辑处理
'''
import json
import requests

from common import get_case_id, derivation, evaluation
from common.mongo import Mongo
from interface.compare import Compare


class Service:
    def __init__(self):
        # 实例化mongo数据的对象
        self.db = Mongo()
    # 发起请求，获取响应
    def make_request(self,data):
        '''
        主要把前端收集过来的数据进行处理，然后发起请求，把响应返回给前端
        核心函数：requests.request()
        :param data: 前端传递过来的数据
        :return: response 响应返回去
        '''
        # 获取method
        method = data.get('method')
        # 获取url的值
        url = data.get('url')
        # 收集参数，cookies，...
        kwargs = {}
        # 对header做校验
        if 'header' in data and data.get('header') != {'': ''} and data.get('header'):
            kwargs['headers'] = data['header']
        # 对params做校验
        if 'params' in data and data.get('params') != {'': ''} and data.get('params'):
            kwargs['params'] = data['params']
        # 对data做校验
        if 'data' in data and data.get('data') != {'': ''} and data.get('data'):
            kwargs['data'] = data['data']
        # 对json做校验--参数数据结构  字典
        if data.get('json'):
            kwargs['json'] = json.loads(data['json'])

        print('kwargs的值是',kwargs)
        response = requests.request(method,url,**kwargs)
        # 如果响应值是字符串的，那么resp.json()就会报错，.text进行解析
        try:
            content = response.json()
        except:
            content = response.text
        data['response']= {
            'code': response.status_code, # 获取状态码
            'json': content   # 获取json数据
        }
        print('发送请求之后的data数据是',data)
        # requests.request()
        return data

    def save_cases(self,data):
        '''
        把前端收集到的data数据保存到数据库中,insert
        :param data:
        :return: insert_id
        '''
        case_id =get_case_id()
        # 把_id放到data数据中
        data.setdefault('_id',case_id)
        # 把data数据插入到mongo数据库中
        id = self.db.insert('interface','cases',data)
        return id

    def make_assert(self,data):
        '''
        {
            "code": "0",
            "data": {
                "brand": "testfan",
                "price": "804",
                "skuId": 1,
                "skuName": "ptest-1",
                "stock": 367
            },
            "message": "success"
        }
        usage:
        表达式                               预期值
        data.brand                         testfan
        data.cross_list.0.name            联谊路--绿溪路
        做比较的时候：反射    运行结果=getattr(对象，method)(参数1，参数2)
        解析表达式
        :param data:
        :return:
        '''
        # 实例化一个做比较的对象
        compare = Compare()
        # 获取各个参数，并解析表达式
        for expr in data['assert']:
            # 预期值
            expect = expr['expected']
            # 预期条件
            condition = expr['condition']
            # 来源
            source= expr['source']
            # 对状态码进行断言
            if source == 'code':
                # tmp 代表的 实际的值
                tmp = str(data['response']['code'])
            else:# 隐藏的含义对body进行断言
                # 实际运行的响应体内容是什么？
                tmp = data['response']['json']
                for item in expr['expression'].split('.'):
                    print('item的值是{},数据类型是{}'.format(item,type(item)))
                    # try:
                    #     # 能走通 证明关键字就是字符串
                    #     tmp=tmp[item]
                    # except:
                    #     # 报错的话，证明这个item是个列表的索引值
                    #     tmp = tmp[int(item)]
                    if isinstance(item,str):
                        tmp = tmp[item]
                    elif isinstance(item,int):
                        tmp = tmp[int(item)]

            # 实际结果跟预期结果做比较，获取最终的值
            result = getattr(compare,condition)(tmp,expect)
            # 把我们的result的结果放到expr这个表达式中
            expr.setdefault('result',result)
        return data

    def team_and_project(self,data):
        '''
        找出variable里面出现的所有的team和project
        去重
        :param data:
        :return: menu  {'产品部':[project1,project2..],'质量部':[,,]}
        '''
        menu = {}
        # 把所有的数据都需要返回过来
        filter = {
            'page':0,
            'limit':0
        }
        results = self.db.search('variable','variable',filter)
        for result in results:
            # 判断一下team这个键是否在result这个字典中，如果不在就追加字典
            if result['team'] not in menu:
                menu.setdefault(result['team'],[result['project']])
            # key in dict  dict【key】追加project
            else:
                menu[result['team']].append(result['project'])
        # todo 键是唯一 team  但是project是列表，需要去重
        for team in menu:
            # 取出所有值，然后去重  之前值=去重之后的值
            menu[team]=list(set(menu[team]))
        print('menu的值是',menu)
        return menu

    # 替换变量
    def replace_variable(self, data):
        '''
        对变量进行解析
        变量的使用：{ip}
        :param data:
        :return: 解析之后的data数据
        '''
        # 过滤条件，然后把所有的变量和值查询出来
        filter = {
            'team':data.get('team'),
            'project':data.get('project')
        }
        results = self.db.search('variable','variable',filter)#[{},{}]
        print('results的值是',results)
        # 把data里面包含的数据提取出来，然后把这些数据跟results的进行比对，解析
        if 'url' in data:
            # {pinter_ip} / pinter / com / getSku
            # todo
            data['url']=derivation(data['url'],results)
        if 'header' in data:
            for key in data['header']:
                data['header'][key] = derivation(data['header'][key],results)

        if 'params' in data:
            for key in data['params']:
                data['params'][key] = derivation(data['params'][key],results)

        if 'data' in data:
            for key in data['data']:
                data['data'][key] = derivation(data['data'][key],results)
        return data

    def interface_list(self,data):
        '''
        接口列表页面提供数据来源
        :return:
        '''
        data = self.db.search('interface','cases',data)
        return data

    def delete(self,data):
        '''
        实现删除功能
        :param data:
        :return:
        '''
        id_list = data.get('id_list')
        filter = {'_id':id_list}
        count = self.db.delete('interface','cases',filter)
        return count


    def interface_search(self,data):
        '''
        编辑页面提供id接口的查询
        :param data:
        :return:
        '''
        filter = {'_id':data.get('id')}
        data = self.db.search('interface','cases',filter)
        return data


    def interface_update(self,data):
        '''
        对接口的数据进行更新
        :param data:
        :return:
        '''
        update_id = self.db.update('interface','cases',{'_id':data.get('id')},data)
        return update_id


    def save_suite(self,data):
        '''
        把套件内容保存到interface-suite表中
        :return:
        '''
        data.setdefault('_id',get_case_id())
        result = self.db.insert('interface','suite',data)
        return result

    def suite_list(self,data):
        '''
        套件页面给table表格提供数据的接口
        :param data:
        :return:
        '''
        print('suite_list的data值是{}'.format(data))
        result = self.db.search('interface', 'suite', data)
        return result

    def suite_delete(self,data):
        '''
        套件删除
        :param data:
        :return:
        '''
        filter = {'_id':data.get('id')}
        result = self.db.delete('interface','suite',filter)
        return result

    def trigger(self,data):
        '''
        实现套件的运行
        :param data:
        :return:
        '''
        print('data的值是{}'.format(data))
        filter = {
            '_id':data.get("id")
        }
        # 通过filter查询到套件的信息
        suite = self.db.search('interface','suite',filter)
        print('suite的值是{}'.format(suite))
        if not suite:
            return filter['_id']
        # 定义一个变量，result->insert report表中的信息
        result={
            '_id':get_case_id(),
            'team':suite[0]['team'],
            'project':suite[0]['project'],
            # 包含case+response的详细信息
            'result': []
        }
        for case_id in suite[0]["cases"]:
            # 通过case_id去cases这个表中查询详细的接口信息
            case = self.db.search('interface','cases',{'_id':case_id})
            print('case的值是{}'.format(case))
            # 调用一个运行接口用例的方法
            case = self.run(case[0])
            #todo 想把case放到report这个表中
            result['result'].append(case)
        # 把result保存到report表中
        self.db.insert('interface','report',result)
        # 返回一个报告的id值
        return result['_id']


    def extract_parameter(self,data):
        '''
        对数据提取的表达式做解析
        e.g data.adcode = sid
        引用 sid => {sid}
        'extract': [{'expression': 'data.adcode', 'expected': 'sid'}]
        1.解析  'data.adcode'
        2. 变量管理的存储方式一样--自己构造
        {name：sid,value:320583}
        :param data:
        :return:
        '''
        print(data)
        if "extract" not in data or not data['extract']:
            return data
        # 参考断言  逻辑一样的
        filter = {
            '_id':get_case_id(),
            'type':'variable',
            'team':data.get('team'),
            'project':data.get('project')
        }
        for extract in data['extract']:
            expr = extract['expression']
            name = extract['expected']
            tmp = data['response']['json']
            for item in expr.split('.'):
                try:
                    tmp = tmp[int(item)]
                except:
                    tmp = tmp[item]
        #todo 1.直接构造variable表  {name：sid,value:tmp}  {sid}
                    #2.g.data
            filter['name']=name
            filter['value']=tmp
            self.db.insert('variable','variable',filter)

        return data

    # 解析关键字，执行代码片段
    def execute_snippet(self,data):
        '''

        普通变量的替换 ${}
        关键字的替换  @{}
        :return:
        '''
        # 查询keyword表，把所有的关键字都查询出来
        results = self.db.search('variable','keyword',{})
        if 'params' in data:
            result = evaluation(data['params'],results)
            # 验签的关键字  sign
            data['params']['sign'] = result

        elif 'data' in data:
            result = evaluation(data['data'], results)
            # 验签的关键字  sign
            data['params']['sign'] = result

        return data



    def run(self,data):
        # 替换变量
        data = self.replace_variable(data)
        # todo 关键字解析-执行代码片段
        data = self.execute_snippet(data)
        # 发起请求
        data = self.make_request(data)
        # 做断言
        data = self.make_assert(data)
        # 提取参数
        data = self.extract_parameter(data)
        return data