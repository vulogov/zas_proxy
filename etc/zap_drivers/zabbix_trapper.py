__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class ZabbixTrapperProtocol:
    def recv(self, buf):
        prit "ZTP *****",buf
    def heartbeat(self):
        return "heartbeat"

def main(env, logger, *args, **argv):
    return ZabbixTrapperProtocol()
