__author__ = 'fuqiang'

from tornado.concurrent import run_on_executor
from  moudle.nmapApi import Snmap
from concurrent.futures import ThreadPoolExecutor

@run_on_executor
def nmapScan(obj):
    return Snmap().nmap_port_sev(obj)