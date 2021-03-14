import json
import re
from common import get_case_id
from common.mongo import Mongo


class Service:
    def __init__(self):
        self.db = Mongo()

    def search(self,data):
        '''
        查询数据库
        :return:
        '''
        collection = data.get('type')
        results = self.db.search('variable',collection,data)
        return results

    def aggregate(self,data):
        '''
        对mongo数据库进行聚合操作,类似于mysql数据库中的分组
        :return:
        '''
        # 获取表名
        collection = data.get('type')
        # 获取key参数，按照哪一个字段(key指向的值)进行聚合
        team = data.get('key')
        # 组合管道
        pipeline = [
            {'$group':{'_id':'$' + team}}
        ]
        # 调用数据库的方法
        data = self.db.aggregate('variable',collection,pipeline)
        return data

    def create(self,data):
        '''
        对数据库进行增加的操作
        :param data:
        :return:
        '''
        collection = data.get('type')
        id = get_case_id()
        data.setdefault('_id',id)
        id = self.db.insert('variable',collection,data)
        return id

    def update(self,data):
        '''
        对数据库进行更新的操作
        :param data:
        :return:
        '''
        collection=data.get('type')
        filter = {
            '_id':data.get('_id')
        }
        update_id = self.db.update('variable',collection,filter,data)
        return update_id
    def delete(self,data):
        '''
        实现删除的功能
        :param data:
        :return:
        '''
        count,id_list = 0, data.get('id_list')
        print('id_list的值是',id_list)
        print('id_list的数据类型是',type(id_list))
        collection = data.get('type')
        for id in id_list:
            delete_id = self.db.delete('variable',collection,{'_id':id})
            count += delete_id
        print('count的值是',count)
        return count

    def debug(self,data):
        '''
        实现关键字调试的功能
        前端自定义的关键字，运行的接口展现出来，然后用alert弹出弹出来
        func = "def test(data):\n    count=100\n    count+=data\n    return count\nresult=test(data)"
        '''
        print('debug函数中传过来的data数据是{}'.format(data))
        print(type(data.get('mock')))
        # 把mock数据转换成字典
        mock = json.loads(data.get('mock'))
        # 以字典的形式传递参数
        content = {'data':mock}
        # 获取代码片段
        snippet = data.get('snippet')
        # 1.判断关键字有无(函数) ---正则表达式匹配2.拼接调用过程
        func = re.findall(r'def\s+(.+?):',snippet)
        if func:
            # 拼接调用过程
            snippet += '\n'+'result='+func[0]
            exec(snippet,content)

        return content['result']

    def save(self,data):
        '''
        实现关键字保存功能
        _id,name-函数的名字,mock-调试数据，snippet:代码(函数的定义+调用)
        keyword这个表中
        :param data:
        :return:
        '''
        mock = json.loads(data.get('mock'))
        snippet = data.get('snippet')
        # 函数的名字，就是关键字的名字
        name = re.findall(r'def\s+(.+?)\(',snippet)
        name = name[0] if name else ""
        # 调用函数
        func = re.findall(r'def\s+(.+?):', snippet)
        if func:
            # 拼接调用过程
            snippet += '\n' + 'result=' + func[0]

        # 把数据保存到数据中
        result = self.db.insert('variable','keyword',{
            '_id':get_case_id(),
            'name':name, # 函数的名字
            'mock':mock, # 调试的数据
            'snippet':snippet # 定义的代码 + 调用过程
        })
        return result