__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class ZabbixTrapperProtocol:
    def recv(self, buf):
        print "ZTP *****",buf


def main(env, logger, *args, **argv):
    return ZabbixTrapperProtocol()
