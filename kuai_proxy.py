"""
单进程抓取快所有代理(免费国内高匿代理)

建表sql
DROP TABLE IF EXISTS `kuai_proxy`;
CREATE TABLE `kuai_proxy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL,
  `port` varchar(10) NOT NULL,
  `type` varchar(10) NOT NULL,
  `location` varchar(30) NOT NULL,
  `response_time` varchar(10) DEFAULT NULL,
  `last_used_time` datetime DEFAULT NULL,
  `is_delete` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `score` varchar(10) NOT NULL DEFAULT '100' COMMENT '分数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=utf8;

插入sql
INSERT INTO `proxy`.`kuai_proxy` (`id`, `ip`, `port`, `type`, `location`, `response_time`, `last_used_time`, `is_delete`, `score`)
 VALUES ('1', '1', '1', '1', '1', '1', '2021-02-02 20:38:10', '1', '100');
"""
import pymysql
import re
from lxml import etree
import requests
import pprint
from mysql_tools import MysqlTools
from datetime import datetime
import time
import random

class KuaiProxy(object):
	def __init__(self):
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
		self.proxies = {}
		self.request_timeout = 5
		self.time_sleep_range = [1, 3]
		self.retry_count = 3
		self.base_page = 'https://www.kuaidaili.com/free/inha'
		self.fail_page_url = []
		# 初始化数据库实例
		self.mysql_tools = MysqlTools(host='127.0.0.1', port=3306, user='root', password='123456', db='proxy', charset='utf8')

	def request_url(self, url):
		time.sleep(random.choice(self.time_sleep_range))
		try:
			response = requests.get(url=url, headers=self.headers, timeout=self.request_timeout)
		except Exception as e:
			if self.retry_count <= 0:
				response = None
				pprint.pprint('<KuaiProxy:request_url()> request fail, url: %s, error: %s' % (url, e))
			else:
				self.retry_count -= 1
				self.request_url(url)
		return response

	def get_page_count(self):
		response = self.request_url(url=self.base_page)
		page_count = None
		if not response:
			pprint.pprint('<KuaiProxy:get_page_count()> get page count fail')
		else:
			# xpath解析
			page_html = response.text
			html = etree.HTML(page_html)
			result_list = html.xpath('//*[@id="listnav"]/ul/li[9]/a/text()')
			if not result_list:
				pprint.pprint('<KuaiProxy:get_page_count()> xpath get rusult fail')
			else:
				page_count = int(result_list[0])
		return page_count

	def get_page_html(self, page_url):
		response = self.request_url(url=page_url)
		page_html = None
		if not response:
			pprint.pprint('<KuaiProxy:get_page_html()> get page html fail')
			self.fail_page_url.append(page_url)
		else:
			page_html = response.text
		return page_html

	def parse_page_html(self, page_html):
		result_list = []
		# 正则解析
		result_list = re.findall(r'<tr>.*?data-title="IP">(.*?)</td>.*?data-title="PORT">(.*?)</td>.*?data-title="匿名度">(.*?)</td>.*?data-title="类型">(.*?)</td>.*?data-title="位置">(.*?)</td>.*?data-title="响应速度">(.*?)</td>.*?data-title="最后验证时间">(.*?)</td>', page_html, re.S)
		if not result_list:
			pprint.pprint('<KuaiProxy:parse_page_html()> parse page html fail')
		return result_list

	def get_sql_cmd(self, result_list):
		# 用批量插入提高效率
		sql_cmd = ''
		values = ''
		try:
			for i in result_list:
				if i != result_list[-1]:
					values += """('%s', '%s', '%s', '%s', '%s', '%s'),""" % (i[0], i[1], i[3], i[4], i[5], i[6])
				else:
					values += """('%s', '%s', '%s', '%s', '%s', '%s')""" % (i[0], i[1], i[3], i[4], i[5], i[6])
			sql_cmd = """INSERT INTO `proxy`.`kuai_proxy` (`ip`, `port`, `type`, `location`, `response_time`, `last_used_time`) VALUES %s;""" % values
		except Exception as e:
			pprint.pprint('<KuaiProxy:get_sql_cmd()> get sql cmd fail, error: %s' % e)
		return sql_cmd

	def save_result2mysql(self, sql_cmd):
		self.mysql_tools.insert_data(sql_cmd)


if __name__ == "__main__":
	begin_time = datetime.now()
	basic_url = 'https://www.kuaidaili.com/free/inha'
	kuai_proxy = KuaiProxy()
	page_count = kuai_proxy.get_page_count()
	if page_count:
		for i in range(1, page_count + 1):
			page_url = basic_url + '/' + str(i)
			page_html = kuai_proxy.get_page_html(url=page_url)
			result_list = kuai_proxy.parse_page_html(page_html)
			sql_cmd = kuai_proxy.get_sql_cmd(result_list)
			kuai_proxy.save_result2mysql(sql_cmd)
	end_time = datetime.now()
	print("任务开始时间: %s, 任务结束时间: %s" % (begin_time, end_time))
