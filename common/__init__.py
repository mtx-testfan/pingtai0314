import time
import uuid
import re

def get_case_id():
    '''
    获取mongo，_id这个字段的值，具有唯一性
    当前时间  time.time()
    uuid
    :return:
    '''
    prefix = time.strftime('%Y%m%d%H%M%S')
    # print(prefix)
    # print(type(uuid.uuid1()))
    u = str(uuid.uuid1())
    # 用-切割成列表，然后进行取值，索引为0,3
    li = u.split('-')
    suffix = li[0]+li[3]
    case_id = prefix + suffix
    return case_id
# {pinter_ip} / pinter / com / getSku
# 替换普通变量
def derivation(data,results):
    '''

    :param data: 前端传过来的数据
    :param results: 从数据库里面查询的所有的变量和值
    :return: 解析之后的data数据
    '''
    # 判断一下关键字里面是否引入了变量 --正则表达是进行提取
    def _exist_variable():
        '''
        {pinter_ip}
        判断一下关键字里面是否引入了变量
        e.g  data=url所对应的值
        :return:
        '''
        variable =re.findall(r'\$\{(.*?)\}',data)
        if variable:
            return variable[0].strip()
        else:
            return None

    # data为空或者数据库里面没有这个变量，就直接返回data数据
    if not data or not results:
        return data

    # 判断变量是否存在
    variable = _exist_variable()
    # 证明引入了变量
    if variable:
        for result in results:
            if variable == result['name']:
                return data.replace('${'+variable+'}',result['value'])

    else:
        return data

# 替换关键字

def evaluation(params,results):
    '''
    提取关键字，然后进行运算，最终得到运算的结果
    :param params:  参数 字典的形式
    :param results:  查询keyword表所得到的的关键字列表
    :return:
    '''
    def _exist_variable(param):
        variable = re.findall(r'\@\{(.*?)\}',param)
        print('evaluation的variable值是',variable)
        # 如果有值
        if variable:
            a = list(map(lambda x:x.strip(),variable))
            print('evaluation的a值是',a)
            return a
        else:
            return None
    if not params or not results:
        return params


    for param in params.values():
        print('遍历出来的param是{}'.format(param))
        # 首先判断param这里面是否有关键字
        variable = _exist_variable(param)
        if variable is None:
            continue
        for v in variable:
            # 遍历从数据库keyword查询出来的结果results
            for result in results:
                if v == result['name']:
                    snippet = result['snippet']
                    content = {'data':{'params':params}}
                    exec(snippet,content)
                    return content['result']
    return params




if __name__ == '__main__':
    # print(get_case_id())
    # get_case_id()
    # get_case_id()
    # get_case_id()
    data = derivation('{pinter_ip}/pinter/com/getSku',[{'name':'pinter_ip','value':'localhost'}])
    print(data)