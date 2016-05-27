__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import struct
from ProtocolDriver import *

class ZabbixProtocol(ProtocolDriver):
    def recv_data(self, data):
        print "RECV",repr(data)
        hdr = struct.unpack("ssssB", data[:5])
        sig = "".join(list(hdr[:4]))
        ver = list(hdr)[-1]
        if sig != "ZBXD":
            return data
        p_len = struct.unpack("L", data[5:13])[0]
        return data[13:13+p_len]
    def send_data(self, data):
        print "RECV",repr(data),type(data)
        hdr="ZBXD"+struct.pack("B",1)+struct.pack("L",len(data)+1)
        return hdr+data+'\n'

def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix", env, logger, ZabbixProtocol, args, argv)

