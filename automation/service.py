# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author:   夭夭 QQ：3512937625
# @Time:   2021-02-28
# @Copyright：北京码同学网络科技有限公司
from automation.keywordFunction import KeyWord
from common import get_case_id
from common.mongo import Mongo
import time

class Service:
	def __init__(self):
		self.db = Mongo()

	def execute(self,commands):
		'''
		getattr
		:param commands:
		:return:
		'''
		print('commands的值是',commands)
		# 关键字库进行实例化
		element = None
		kw = KeyWord() # 对象
		for command in commands:
			element = getattr(kw,command['command'])(element,command['parameter'])
			# 加个等待，代码更稳定
			time.sleep(3)
		kw.base_quit_driver()

	def save(self, data):
		'''
		保存功能
		:return:
		'''
		data.setdefault('_id',get_case_id())
		return self.db.insert('automation','cases',data)