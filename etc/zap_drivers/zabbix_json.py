__author__ = 'gandalf'

from ProtocolDriver import *

class ZabbixJson(ProtocolDriver):
    pass

def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_json", env, logger, ZabbixJson, args, argv)

