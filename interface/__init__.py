from flask import Blueprint,render_template,request,jsonify
# 创建蓝图对象
from interface.service import Service

interface =Blueprint('interface',
          __name__,
          static_folder='static',
          template_folder='templates',
          url_prefix='/interface')

# 创建路由返回创建接口/interface/create---对应的资源信息
@interface.route('/create')
def index():
    return render_template('interface.html')

# 定义'/interface/api/v1/debug'这个路由
@interface.route('/api/v1/debug',methods=['POST'])
def api_v1_debug():
    # 获取前端传来的数据
    data=request.get_json()
    print('前端传递过来的数据是',data)
    # 数据校验 method和url地址必须要传过来
    method = data.get('method')
    if not method:
        return jsonify({
            'status':400,
            'message':'invalid method parameter',
            'data':data
        })
    url = data.get('url')
    if not url:
        return jsonify({
            'status':400,
            'message':'invalid url parameter',
            'data':data
        })
    # 对数据做逻辑处理 在servicepython文件中做处理
    server = Service()
    # todo 发起请求之前，变量解析
    # data = server.replace_variable(data)
    # data =server.make_request(data)
    # # 对响应结果做断言
    # data = server.make_assert(data)

    data = server.run(data)

    # 给前端返回数据
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })

@interface.route('/api/v1/save',methods=['POST'])
def api_v1_save():
    # 获取前端传来的数据
    data = request.get_json()
    print('前端传递过来的数据是', data)
    # 数据校验 method和url地址必须要传过来
    method = data.get('method')
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid method parameter',
            'data': data
        })
    url = data.get('url')
    if not url:
        return jsonify({
            'status': 400,
            'message': 'invalid url parameter',
            'data': data
        })
    # 对数据做逻辑处理



    # 给前端返回数据
    try:
        # 把数据保存到数据库中
        id = Service().save_cases(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': id
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'message': e,
            'data': data
        })


@interface.route('/api/v1/team_and_project')
def api_v1_team_and_project():
    # 获取前端传来的数据
    data = request.values.to_dict()

    # 给前端返回数据
    try:
        # 把数据保存到数据库中
        data = Service().team_and_project(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'message': e,
            'data': data
        })

#展现接口列表页面的路由
@interface.route('/list')
def list():
    return render_template('interface_list.html')
# /interface/api/v1/search 接口列表页提供数据
@interface.route('/api/v1/search')
def api_v1_search():
    data = request.values.to_dict()
    print(data)
    service = Service()
    data = service.interface_list(data)
    return jsonify({
        'status':0,
        'message':'ok',
        'data':data
    })



# 实现删除功能
@interface.route('/api/v1/delete',methods=['POST'])
def api_v1_delete():
    # 获取前端传来的数据
    data = request.get_json()
    print('前端传递过来的数据是', data)
    # 数据校验 method和url地址必须要传过来
    id_list = data.get('id_list')
    if not id_list:
        return jsonify({
            'status': 400,
            'message': 'invalid id_list parameter',
            'data': data
        })


    # 给前端返回数据
    try:
        # 把数据从数据库中删除
        id = Service().delete(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': id
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'message': e,
            'data': data
        })

# 对接口进行编辑
@interface.route('/edit/<id>')
def edit(id):
    return render_template('interface_edit.html')



# 编辑页面实现数据查询
@interface.route('/api/v2/search')
def api_v2_search():
    data = request.values.to_dict()
    if 'id' not in data:
        return jsonify({
            'status': 400,
            'message': 'invalid id parameter',
            'data': data
        })

    service = Service()
    data = service.interface_search(data)
    return jsonify({
        'status':0,
        'message':'ok',
        'data':data
    })

@interface.route('/api/v1/update',methods=['POST'])
def api_v1_update():
    data = request.get_json()

    print('data的值是',data)
    id = data.get('id')
    print('id的值是',id)
    if not id:
        return jsonify({
            'status': 400,
            'message': 'invalid id parameter',
            'data': data
        })
    service = Service()
    data = service.interface_update(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })

@interface.route('/api/v1/suite',methods=['POST'])
def api_v1_suite():
    # 获取前端传来的数据
    data = request.get_json()
    print('前端传递过来的数据是', data)
    team = data.get('team')
    if not team:
        return jsonify({
            'status': 400,
            'message': 'invalid team parameter',
            'data': data
        })
    project = data.get('project')
    if not project:
        return jsonify({
            'status': 400,
            'message': 'invalid project parameter',
            'data': data
        })
    cases = data.get('cases')
    if not cases:
        return jsonify({
            'status': 400,
            'message': 'invalid cases parameter',
            'data': data
        })
    # 给前端返回数据
    try:
        # 把数据保存到数据中
        id = Service().save_suite(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': id
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'message': e,
            'data': data
        })

# 展现套件的页面
@interface.route('/suite')
def suite():
    return render_template('interface_suite.html')

@interface.route('/api/v1/suite/list')
def api_v1_suite_list():
    data = request.values.to_dict()
    print(data)
    service = Service()
    data = service.suite_list(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })

@interface.route('/api/v1/suite/delete',methods=['POST'])
def api_v1_suite_delete():
    '''套件删除功能'''
    data = request.get_json()
    case_id = data.get('id')
    if not case_id:
        return jsonify({
            'status': 400,
            'message': 'invalid case_id parameter',
            'data': data
        })
    service = Service()
    data = service.suite_delete(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })

@interface.route('/api/v1/trigger')
def api_v1_trigger():
    data = request.values.to_dict()
    case_id = data.get('id')
    if not case_id:
        return jsonify({
            'status': 400,
            'message': 'invalid case_id parameter',
            'data': data
        })

    service = Service()
    data = service.trigger(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })