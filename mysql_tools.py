"""
mysql封装
"""

import pymysql
from pprint import pprint


class MysqlTools():
	def __init__(self, host='127.0.0.1', port=3306, user='root', password='123456', db='test', charset='utf8'):
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.db = db
		self.charset = charset
		self.connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)
		self.cursor = self.connect.cursor()


	def insert_data(self, sql_cmd):
		flag = True
		try:
			self.cursor.execute(sql_cmd)
			self.connect.commit()
		except Exception as e:
			flag = False
			pprint("<MysqlTools:insert_data()> insert data fail, sql_cmd: %s, error: %s" % (sql_cmd, e))
			self.connect.rollback()
		return flag

	def query_data(self, sql_cmd):
		result_list = []
		try:
			self.cursor.execute(sql_cmd)
			result_list = self.cursor.fetchall()
		except Exception as e:
			pprint("qurey data fail: %s" % e)
			self.connect.rollback()
		return result_list

	def close_connect(self):
		if self.connect:
			self.cursor.close()
			self.connect.close()