__author__ = 'gandalf'


class ZabbixProtocol:
    def __init__(self, creator):
        self.creator = creator
        self.env = self.creator.env
        self.logger = self.creator.logger
        self.args = self.creator.args
        self.argv = self.creator.argv
    def recv(self, buf):
        print "ZTP *****",buf
    def send(self):
        return "***"

class ZabbixProtocolCreator:
    def __init__(self, env, logger, args, argv):
        self.env = env
        self.logger = logger
        self.args = args
        self.argv = argv
    def driver(self):
        return ZabbixProtocol(self)



def main(env, logger, *args, **argv):
    return ZabbixProtocolCreator(env, logger, args, argv)