import time
import os
import codecs
from logging import FileHandler
import threading
import logging
from multiprocessing import Process
import random



class SafeFileHandler(FileHandler):
    def __init__(self, filename, mode, encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        """
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_baseFilename(record):
                self.build_baseFilename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_baseFilename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
                self.baseFilename + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def build_baseFilename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()


class LoggingTools(object):
    _instance = None
    _is_init = False
    _instance_lock = threading.Lock()

    def __init__(self, log_name='app_log', log_level=logging.DEBUG, file_path=r'C:\Users\mi\Desktop', file_name='test_app.log'):
        if not LoggingTools._is_init:
            LoggingTools._is_init = True
            self.log_name = log_name  # 可定位到哪个模块记录的日志
            self.log_level = log_level
            self.file_path = file_path
            self.file_name = file_name
            self.logger = logging.getLogger(self.log_name)  # logger = logging.getLogger(__name__)可记录日志产生的模块
            self.formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                               datefmt='%Y-%m-%d %H:%M:%S')
            # 终端输出
            self.stream_handler = logging.StreamHandler(stream=None)  # sys.stderr
            # self.stream_handler.setLevel(self.log_level) # 这里不生效
            self.stream_handler.setFormatter(self.formatter)
            # 文件输出
            self.file_handler = SafeFileHandler(filename=os.path.join(self.file_path, self.file_name), mode='a',
                                                    encoding='utf8')
            # self.file_handler.setLevel(self.log_level) # 这里不生效
            self.file_handler.setFormatter(self.formatter)
            self.logger.setLevel(self.log_level)  # 这里设置才生效,默认为WARNING级别
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

        :param info:
        :param log_level:
        :return:
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


def test_write():
    my_log = LoggingTools()
    for i in range(120):
        time.sleep(random.choice([0.1, 0.5, 1, 1.5, 2]))
        my_log.writer_log("hello world: process(%s) >>>>>> %s" % (os.getpid(), str(i)))

if __name__ == "__main__":
    # my_log = LoggingTools()
    # for i in range(30):
    #     time.sleep(random.randint(1, 3))
    #     my_log.writer_log("hello wrold: %s" % str(i))

    p1 = Process(target=test_write, args=())
    p2 = Process(target=test_write, args=())
    p3 = Process(target=test_write, args=())
    p4 = Process(target=test_write, args=())
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print("over over over over over")
    with open(r'C:\Users\mi\Desktop\test_app.log.2021-03-12', 'r') as fr:
        lines = fr.readlines()
        print(len(lines))