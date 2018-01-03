# -*- coding: utf-8 -*-
'''
@author: Tingting He
@version: 1.0.0
'''

import os
import logging

from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class CheckType(object):
    def __init__(self):
        self.log = self.create_logger(log_to_standard_output=True)
        self.critical = self.log.critical
        self.fatal = self.log.fatal
        self.error = self.log.error
        self.warning = self.log.warning
        self.warn = self.log.warn
        self.info = self.log.info
        self.debug = self.log.debug
        self.exception = self.log.exception

    def create_logger(self, log_file_name='./skeleton_running.log',
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
            if os.path.exists(log_file_name):
                os.remove(log_file_name)

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
