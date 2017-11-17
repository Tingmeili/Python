# encoding: utf-8
'''
hook logging for format log style

Create on May 27, 2017
@author: Hongping Wang
@change: 2017-06-01 Hongping Wang: initialization
         2017-06-06 Hongping Wang: support write a new log file every day
         2017-07-27 Qiangqiang Wei: support the log for different project
         2017-07-28 Qiangqiang Wei: create the new log_base.py and move the code to this script
         2017-11-04 Hongping Wang: support write log to file and standard output synchronously
'''
import os
import logging

from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

import config

class AutoTestLog():
    '''
    The auto test log
    '''

    def create_logger(self, log_file_name='{0}/e2etest_running.log'.format(config.BASE_DIR),
                      log_level=logging.DEBUG,
                      log_date_format='%Y-%m-%d %H:%M:%S%z',
                      log_formater='%(asctime)s %(filename)s:%(funcName)s %(levelname)s [line:%(lineno)d] %(message)s',
                      max_log_files=3,
                      one_day_one_file=True,
                      max_log_file_size=10485760,
                      log_to_standard_output=False
                      ):
        '''
        @summary: create the logger
        @param log_file_name: the log file name, should be absolute path. default value is /tmp/vamp/videocenter_running.log
                             if the value is None or "", print the log to standard output
        @param log_level: Integer of the log level. default value is logging.DEBUG
        @param max_log_files: the max number of files. It is valid when one_day_one_file equal False. default value is 3
        @param one_day_one_file: whether only create a file in one day. default value is True, one day one log file
        @param max_log_file_size: the max size of the log file. unit is byte. default value is 10 MB
        @param log_date_format: String of log date format. default value is '%Y-%m-%d %H:%M:%S%z', like 2017-06-01 11:44:06+0000
        @param log_to_standard_output: whether print logs into standard output, this argument will ignore log_file_name value
        @return: the logger
        '''
        # initialize log file
        if log_file_name:
            log_file_name = os.path.abspath(log_file_name)  # change path to absolute path
            if not os.path.exists(os.path.dirname(log_file_name)):
                os.makedirs(os.path.dirname(log_file_name))

        # write log into file or standard output
        if log_file_name and type(log_file_name) == type('') and log_file_name != '':
            # write log to file
            logger = logging.getLogger(log_file_name)
            logger.setLevel(log_level)

            # write a new log file every day
            if one_day_one_file:
                Rthandler = TimedRotatingFileHandler(log_file_name, when='D', backupCount=max_log_files)
            else:
                Rthandler = RotatingFileHandler(log_file_name, maxBytes=max_log_file_size, backupCount=max_log_files)
            formatter = logging.Formatter(fmt=log_formater, datefmt=log_date_format)
            Rthandler.setFormatter(formatter)
            logger.addHandler(Rthandler)

            # write log to standard output synchronously
            if log_to_standard_output:
                console = logging.StreamHandler()
                console.setLevel(log_level)
                console.setFormatter(formatter)
                logger.addHandler(console)

        # write log to standard output default
        else:
            logging.basicConfig(level=log_level, format=log_formater, datefmt=log_date_format)
            logger = logging

        return logger

# define application log file path
__log = AutoTestLog().create_logger(log_to_standard_output=True)
critical = __log.critical
fatal = __log.fatal
error = __log.error
warning = __log.warning
warn = __log.warn
info = __log.info
debug = __log.debug
exception = __log.exception



#1.日志等级分别有以下几种：

  #CRITICAL : 'CRITICAL',
  #ERROR : 'ERROR',
  #WARNING : 'WARNING',
  #INFO : 'INFO',
  #DEBUG : 'DEBUG',
  #NOTSET : 'NOTSET',

  #一旦设置了日志等级，则调用比等级低的日志记录函数则不会输出
   #设置日志的步骤:handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
   #fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

   #formatter = logging.Formatter(fmt)   # 实例化formatter
   #handler.setFormatter(formatter)      # 为handler添加formatter

   #logger = logging.getLogger('tst')    # 获取名为tst的logger
   #logger.addHandler(handler)           # 为logger添加handler
   #logger.setLevel(logging.DEBUG)









#2. 自python2.6开始，新增了一种格式化字符串的函数str.format()，可谓威力十足
     #花括号声明{}、用于渲染前的参数引用声明， 花括号里可以用数字代表引用参数的序号， 或者 变量名直接引用。
     #log_file_name='{0}/e2etest_running.log'.format(config.BASE_DIR)
     # 例1：  data = {'first': 'Hodor', 'last': 'Hodor!'}
             # old: '%(first)s %(last)s' % data
             # new:  '{first} {last}'.format(**data)
             #output: Hodor Hodor1

     # 例2:
        #'{:^10}'.format('test')
        #output: '   test   '
        #'{:<10}'.format('test')
        # output:'test      '



# 3.TimedRotatingFileHandler:
    # TimedRotatingFileHandler(filename [,when [,interval [,backupCount]]])
         #filename 是输出日志文件名的前缀
         #when 是一个字符串的定义如下：
          #“S”: Seconds
          #“M”: Minutes
          #“H”: Hours
          #“D”: Days
          #“W”: Week day (0=Monday)
          #“midnight”: Roll over at midnight
        #backupCount 是保留日志个数。默认的0是不会自动删除掉日志。若设3，则在文件的创建过程中
        #库会判断是否有超过这个3，若超过，则会从最先创建的开始删除。
    #RotatingFileHandler:

