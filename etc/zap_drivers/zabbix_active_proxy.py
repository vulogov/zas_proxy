__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from ProtocolDriver import *

class ZabbixActiveProxyProtocol(ProtocolDriver):
    def send_heartbeat(self):
        return self.toChain("proxy heartbeat")
    def send_data(self, data):
        print "###",data
        return {"request": data, "host": self.name}


def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_active_proxy", env, logger, ZabbixActiveProxyProtocol, args, argv)
