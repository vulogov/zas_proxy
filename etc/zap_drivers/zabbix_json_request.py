__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from ProtocolDriver import *

class ZabbixJsonRequest(ProtocolDriver):
    def send_data(self, data):
        print "###",data
        return {"request": data}


def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_json_request", env, logger, ZabbixJsonRequest, args, argv)