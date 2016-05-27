__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import time
import simplejson
from ProtocolDriver import *

class ZabbixJsonHost(ProtocolDriver):
    def recv_data(self, data):
        return data
    def send_data(self, data):
        import time
        data["host"] = str(self.ctx["host"])
        return data



def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_json_host", env, logger, ZabbixJsonHost, args, argv)