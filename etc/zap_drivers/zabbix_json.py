__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import simplejson
from ProtocolDriver import *

class ZabbixJson(ProtocolDriver):
    def send_data(self, data):
        buffer = simplejson.dumps(data)
        return buffer
    def recv_data(self, data):
        return simplejson.loads(data)


def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_json", env, logger, ZabbixJson, args, argv)

