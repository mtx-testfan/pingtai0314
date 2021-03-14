# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author:   夭夭 QQ：3512937625
# @Time:   2021-02-28
# @Copyright：北京码同学网络科技有限公司
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
class KeyWord:
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()

	# 找元素的方法
	def find(self, el,parameter):
		'''
		'''
		by = parameter.get('by')
		selector = parameter.get('selector')

		# x指的是driver
		el = WebDriverWait(self.driver, timeout=30, poll_frequency=1) \
			.until(lambda x: x.find_element(by,selector))
		return el

	# 点击
	def click(self, el, parameter):
		# 找到元素,点击
		el.click()
		return el

	# 输入
	def send(self, el, parameter):
		value = parameter.get('value')
		# 清空
		el.clear()
		# 输入
		el.send_keys(value)
		return el

	# 打开
	def get(self, el, parameter):
		value = parameter.get('value')
		self.driver.get(value)
		return el

	# 等待
	def wait(self, el, parameter):
		'''
		从excel中读取的值默认都是字符串格式的
		:param el:
		:param value:
		:return:
		'''
		value = parameter.get('value')
		time.sleep(int(value))
		return el

	def base_quit_driver(self):
		self.driver.quit()


if __name__ == '__main__':
	pass
