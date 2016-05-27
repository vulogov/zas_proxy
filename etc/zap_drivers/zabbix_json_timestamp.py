__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import simplejson
from ProtocolDriver import *

class ZabbixJsonTimestamp(ProtocolDriver):
    def send_data(self, data):
        import time
        data["clock"] = time.time()
        return data



def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_json_timestamp", env, logger, ZabbixJsonTimestamp, args, argv)

