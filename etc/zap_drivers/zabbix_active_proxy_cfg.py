__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from ProtocolDriver import *

class ZabbixActiveProxyCfgProtocol(ProtocolDriver):
    def cfg2dict(self, cfg):
        fields = cfg["fields"]
        out = []
        for c in cfg["data"]:
            d = {}
            count=0
            for k in fields:
                d[k] = c[count]
                count += 1
            out.append(d)
        return out
    def recv_data(self, data):
        host = self.ctx["host"]
        drv = self.env.db_link("config")
        for i in self.cfg2dict(data["globalmacro"]):
            drv.set_value("%s:%s"%(host, i["macro"]), "globalmacro", i)
        _hosts = self.cfg2dict(data["hosts"])
        hosts = {}
        for i in _hosts:
            hosts[i["hostid"]] = i
            drv.set_value("%s:%s"%(host,i["name"]), "host", i)
        print hosts
        return data
    def send_data(self, data):
        return data


def main(env, logger, *args, **argv):
    return ProtocolDriverCreator("zabbix_active_proxy_cfg", env, logger, ZabbixActiveProxyCfgProtocol, args, argv)
