__author__ = 'gandalf'

from ProtocolDriver import *

class ZabbixProtocol(ProtocolDriver):
    pass



def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix", env, logger, ZabbixProtocol, args, argv)