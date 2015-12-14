#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import logging
import datetime
from logging.handlers import BaseRotatingHandler

if __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

class LogHandler(BaseRotatingHandler):
    def __init__(self, filename, maxbytes=2*1024, mode='a', encoding=None, delay=0):
        self.mode = mode
        self.index = 0
        self.maxBytes = maxbytes
        self.createdate = datetime.datetime.now().strftime("%Y%m%d")
        BaseRotatingHandler.__init__(self, filename, mode, encoding, delay)

    def shouldRollover(self, record):
        if self.stream is None:
            self.stream = self._open()
        if datetime.datetime.now().strftime("%Y%m%d") != self.createdate:
            return 1
        if self.maxBytes > 0:
            msg = "%s\n"%self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) > self.maxBytes:
                return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
            dfn = self.baseFilename + '_' + self.createdate + '_' + str(self.index)
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
        self.stream = self._open()
        curdate = datetime.datetime.now().strftime("%Y%m%d")
        if curdate == self.createdate:
            self.index += 1
        else:
            self.createdate = curdate
            self.index = 0

class Logger(logging.Logger):
    """maybe just revalue logging._srcfile"""
    def findCaller(self):
        f = logging.currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

class LogMixin(object):
    fmt = "[%(asctime)s-%(levelname)s-%(filename)s-%(lineno)d]-%(message)s"
    
    def init_logger(self):
        if hasattr(self.__class__, "_logger_inited"): return
        logging.setLoggerClass(Logger)
        fmt = logging.Formatter(self.fmt)
        level_names = dict(debug=logging.DEBUG,info=logging.INFO,warning=logging.WARNING,error=logging.ERROR)
        for n, l in level_names.items():
            tmp_log = logging.getLogger(n)
            tmp_log.setLevel(l)
            if hasattr(self.__class__, "_log_to_file"):
                handler = LogHandler(getattr(self.__class__, "_log_to_file"))
            else:
                handler = logging.StreamHandler()
            handler.setFormatter(fmt)
            tmp_log.addHandler(handler)
            setattr(self.__class__, n, tmp_log)
        setattr(self.__class__, "_logger_inited", True)

    def set_format(self, fmt_str):
        self.fmt = fmt_str

    def get_logger(self, level_name):
        self.init_logger()
        return getattr(self.__class__, level_name)

    def log_debug(self, msg, *args, **kwargs):
        self.get_logger("debug").debug(msg, *args, **kwargs)

    def log_info(self, msg, *args, **kwargs):
        self.get_logger("info").info(msg, *args, **kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.get_logger("warning").warning(msg, *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.get_logger("error").error(msg, *args, **kwargs)

    def log_exception(self, msg, *args, **kwargs):
        self.get_logger("error").exception(msg, *args, **kwargs)

class Loggerer(LogMixin):
    
    def __init__(self, log_file=None):
        if log_file :
            Loggerer._log_to_file = log_file
        LogMixin.__init__(self)


default = Loggerer()

def initialize(filename):
    default = Loggerer(filename)

def log_info(msg, *args, **kwargs):
    default.log_info(msg, *args, **kwargs)

def log_debug(msg, *args, **kwargs):
    default.log_debug(msg, *args, **kwargs)

def log_error(msg, *args, **kwargs):
    default.log_error(msg, *args, **kwargs)

def log_warning(msg, *args, **kwargs):
    default.log_warning(msg, *args, **kwargs)

def log_exception(msg, *args, **kwargs):
    default.log_exception(msg, *args, **kwargs)
    

def test():
    initialize("tmp_log.log")
    for i in xrange(20000):
        log_debug("log_debug")
        log_error("log_error")
        log_warning("log_warning")
        log_info("log_info")


if __name__=="__main__":
    test() 
