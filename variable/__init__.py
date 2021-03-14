# 创建蓝图
from flask import Blueprint, render_template, request, jsonify

from variable.service import Service

variable=Blueprint('variable',
          __name__,
          static_folder='static',
          template_folder='templates',
          url_prefix='/variable')
# 创建蓝图，展现变量管理的页面
@variable.route('/')
def index():
    return render_template('variable.html')

# 主要是查询team的数据
@variable.route('/api/v1/aggregate',methods=['POST'])
def api_v1_aggregate():
    # 获取参数
    data = request.get_json()
    # 参数校验

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid type parameter',
            'data': data
        })
    if 'key' not in data or not data['key']:
        return jsonify({
            'status': 400,
            'message': 'invalid key parameter',
            'data': data
        })

    # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().aggregate(data)
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



@variable.route('/api/v1/search')
def api_v1_search():
    # 获取参数
    data = request.values.to_dict()
    #参数校验

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid type parameter',
            'data': data
        })

    # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().search(data)
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

# 调用数据库的insert方法
@variable.route('/api/v1/create',methods=['POST'])
def api_v1_create():
    # 获取参数
    data = request.get_json()
    #参数校验

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid type parameter',
            'data': data
        })
    if 'team' not in data or not data['team']:
        return jsonify({
            'status': 400,
            'message': 'invalid team parameter',
            'data': data
        })
    if 'project' not in data or not data['project']:
        return jsonify({
            'status': 400,
            'message': 'invalid project parameter',
            'data': data
        })
    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': 'invalid name parameter',
            'data': data
        })
    if 'value' not in data or not data['value']:
        return jsonify({
            'status': 400,
            'message': 'invalid value parameter',
            'data': data
        })

    # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().create(data)
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


# 修改
@variable.route('/api/v1/update',methods=['POST'])
def api_v1_update():
    # 获取参数
    data = request.get_json()
    # 参数校验
    if '_id' not in data or not data['_id']:
        return jsonify({
            'status': 400,
            'message': 'invalid _id parameter',
            'data': data
        })

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid type parameter',
            'data': data
        })
    if 'team' not in data or not data['team']:
        return jsonify({
            'status': 400,
            'message': 'invalid team parameter',
            'data': data
        })
    if 'project' not in data or not data['project']:
        return jsonify({
            'status': 400,
            'message': 'invalid project parameter',
            'data': data
        })
    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': 'invalid name parameter',
            'data': data
        })
    if 'value' not in data or not data['value']:
        return jsonify({
            'status': 400,
            'message': 'invalid value parameter',
            'data': data
        })

    # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().update(data)
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

# 删除
@variable.route('/api/v1/delete',methods=['POST'])
def api_v1_delete():
    # 获取参数
    data = request.get_json()
    print('data的数据是',data)
    # 参数校验
    if 'id_list' not in data or not data['id_list']:
        return jsonify({
            'status': 400,
            'message': 'invalid id_list parameter',
            'data': data
        })

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid type parameter',
            'data': data
        })

    # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().delete(data)
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
@variable.route('/keyword')
def keyword():
    return render_template('keyword.html')

@variable.route('/api/v1/debug',methods=['POST'])
def api_v1_debug():
    # 获取数据
    data = request.get_json()
    # 参数的校验

    # 参数校验
    if 'mock' not in data or not data['mock']:
        return jsonify({
            'status': 400,
            'message': 'invalid  mock parameter',
            'data': data
        })


    if 'snippet' not in data or not data['snippet']:
        return jsonify({
            'status': 400,
            'message': 'invalid snippet parameter',
            'data': data
        })


        # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().debug(data)
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



@variable.route('/api/v1/save',methods=['POST'])
def api_v1_save():
    # 获取数据
    data = request.get_json()
    # 参数校验
    if 'mock' not in data or not data['mock']:
        return jsonify({
            'status': 400,
            'message': 'invalid  mock parameter',
            'data': data
        })


    if 'snippet' not in data or not data['snippet']:
        return jsonify({
            'status': 400,
            'message': 'invalid snippet parameter',
            'data': data
        })


        # 给前端返回数据
    try:
        # 逻辑处理：查询数据库
        data = Service().save(data)
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