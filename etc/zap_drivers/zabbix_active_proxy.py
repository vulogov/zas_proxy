__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from ProtocolDriver import *

class ZabbixActiveProxyProtocol(ProtocolDriver):
    pass


def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_active_proxy", env, logger, ZabbixActiveProxyProtocol, args, argv)
