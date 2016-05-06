__author__ = 'gandalf'

import simplejson
from ProtocolDriver import *

class ZabbixJson(ProtocolDriver):
    def recv_data(self, data):
        return simplejson.dumps(data)
    def recv_data(self, data):
        return simplejson.loads(data)


def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_json", env, logger, ZabbixJson, args, argv)

