__author__ = 'fuqiang'

from tornado.concurrent import run_on_executor
from  moudle.nmapApi import Snmap


@run_on_executor
def nmapScan(obj):
    return Snmap().nmap_port_sev(obj)