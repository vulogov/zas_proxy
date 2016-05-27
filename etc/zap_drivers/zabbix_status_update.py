__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import time
import simplejson
from ProtocolDriver import *

class ZabbixStatusUpdate(ProtocolDriver):
    def recv_data(self, data):
        drv = self.env.db_link("status")
        if drv != None:
            if not data.has_key("response") or data["response"] != "success":
                drv.set(self.ctx["host"], "status", status=False, stamp=time.time())
            else:
                drv.set(self.ctx["host"], "status", status=True, stamp=time.time())
        return data
    def send_data(self, data):
        return data

def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_status_update", env, logger, ZabbixStatusUpdate, args, argv)