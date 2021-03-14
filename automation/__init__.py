# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author:   夭夭 QQ：3512937625
# @Time:   2021-02-28
# @Copyright：北京码同学网络科技有限公司
from flask import Blueprint,render_template,jsonify,request

from automation.service import Service

automation = Blueprint('automation',
		  __name__,
		  static_folder='static',
		  template_folder='templates',
		  url_prefix='/automation/')

@automation.route('/')
def index():
	return render_template('automation.html')


@automation.route('/api/v1/run',methods=['POST'])
def api_v1_run():
	data = request.get_json()
	if 'casename' not in data or not data.get('casename'):
		return jsonify({
			'status':400,
            'message':'invalid casename parameter',
            'data':data
		})
	if 'commands' not in data or not data.get('commands'):
		return jsonify({
			'status': 400,
			'message': 'invalid commands parameter',
			'data': data
		})
	try:
		# 把数据保存到数据库中
		Service().execute(data['commands'])
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

@automation.route('/api/v1/save',methods=['POST'])
def api_v1_save():
	data = request.get_json()
	if 'casename' not in data or not data.get('casename'):
		return jsonify({
			'status':400,
            'message':'invalid casename parameter',
            'data':data
		})
	if 'commands' not in data or not data.get('commands'):
		return jsonify({
			'status': 400,
			'message': 'invalid commands parameter',
			'data': data
		})
	try:
		# 把数据保存到数据库中
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