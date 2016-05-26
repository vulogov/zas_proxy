__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import struct
from ProtocolDriver import *

class ZabbixNS(ProtocolDriver):
    def recv_data(self, data):
        return data
    def send_data(self, data):
        data["ns"] = 0
        return data

def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_ns_stamp", env, logger, ZabbixNS, args, argv)

