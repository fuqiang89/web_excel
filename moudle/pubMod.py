__author__ = 'Administrator'
import logging
import datetime
import sys,re
import functools
import cStringIO
import traceback



def LogMod(fname="fname",Path="",Cutlog=False):
    if Cutlog == False:
        fname=Path + fname
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=fname,
                     filemode='a')
    else:
        daytime=datetime.datetime.now().strftime('%Y-%m-%d')
        fname=Path + fname + daytime
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=fname,
                     filemode='a')
    return logging

def catch_exception(func):
    """装饰器
    捕获异常"""
    @functools.wraps(func)
    def t(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:#打印所有未知异常
            err_fp = cStringIO.StringIO() #创建内存文件对象
            traceback.print_exc(file=err_fp)
            err_msg = err_fp.getvalue()
            err_msg='\n'.join(err_msg.split( '\n'))
            print('\nargs:\n%s\nkwargs:\n%s\nerr_msg:\n%s\n'%(str(args),str(kwargs),err_msg))
            return  err_msg
    return t
