import logging
import os
from logging import handlers
import time


class Logger(object):
    file_name = '/logs/' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.log'
    # 获取当前的文件路径
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, level='debug', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        # print('日志的存储路径：' + self.log_path + self.file_name)
        self.logger = logging.getLogger(name=self.file_name)
        # 日志重复打印 [ 判断是否已经有这个对象，有的话，就再重新添加]
        if not self.logger.handlers:
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)

            format_str = logging.Formatter(fmt)  # 设置日志格式
            self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            th = handlers.TimedRotatingFileHandler(filename=self.log_path + self.file_name, when=when,
                                                   backupCount=backCount,
                                                   encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
            th.setFormatter(format_str)  # 设置文件里写入的格式
            self.logger.addHandler(sh)  # 把对象加到logger里
            self.logger.addHandler(th)


if __name__ == '__main__':
    log = Logger()
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    # Logger('error.log', level='error').logger.error('error')
