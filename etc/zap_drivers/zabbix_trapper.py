__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from ProtocolDriver import *

class ZabbixTrapperProtocol(ProtocolDriver):
    pass

def main(env, logger, *args, **argv):
    return ProtocolDriverCreator('zabbix_trapper', env, logger, ZabbixTrapperProtocol, args, argv)
