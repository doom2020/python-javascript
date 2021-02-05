"""
日志工具封装，单例模式
"""

import logging
import os
import threading


class LoggingTools(object):
	_instance = None
	_is_init = False
	_instance_lock = threading.Lock()
	def __init__(self, log_name='app_log', log_level=logging.DEBUG, file_path= '/app/data/log', file_name='app.log'):
		if not LoggingTools._is_init:
			LoggingTools._is_init = True
			self.log_name = log_name # 可定位到哪个模块记录的日志
			self.log_level = log_level
			self.file_path = file_path
			self.file_name = file_name
			self.logger = logging.getLogger(self.log_name) # logger = logging.getLogger(__name__)可记录日志产生的模块
			self.formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
			# 终端输出
			self.stream_handler = logging.StreamHandler(stream=None) # sys.stderr
			# self.stream_handler.setLevel(self.log_level) # 这里不生效
			self.stream_handler.setFormatter(self.formatter)
			# 文件输出
			self.file_handler = logging.FileHandler(filename=os.path.join(self.file_path, self.file_name), mode='a', encoding='utf8')
			# self.file_handler.setLevel(self.log_level) # 这里不生效
			self.file_handler.setFormatter(self.formatter)
			self.logger.setLevel(self.log_level) # 这里设置才生效,默认为WARNING级别
			# add handler to logger
			self.logger.addHandler(self.stream_handler)
			self.logger.addHandler(self.file_handler)

	def __new__(cls, *args, **kwargs):
		if LoggingTools._instance is None:
			with LoggingTools._instance_lock:
				if LoggingTools._instance is None:
					LoggingTools._instance = super().__new__(cls)
		return LoggingTools._instance

	def writer_log(self, info, log_level='debug'):
		"""
		写日志
		"""
		if log_level == 'debug':
			self.logger.debug(info)
		elif log_level == 'info':
			self.logger.info(info)
		elif log_level == 'warning':
			self.logger.warning(info)
		elif log_level == 'error':
			self.logger.error(info)
		elif log_level == 'critical':
			self.logger.critical(info)

if __name__ == "__main__":
	logger = LoggingTools(file_path=r'C:\Users\mi\Desktop')
	logger.writer_log('hello world', log_level='debug')
	logger.writer_log('hello world2', log_level='info')
	logger.writer_log('hello world3', log_level='warning')
	logger.writer_log('hello world4', log_level='error')
	logger.writer_log('hello world5', log_level='critical')

