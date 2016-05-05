__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class Heartbeat:
    def __init__(self, env, proc, args, argv):
        self.env = env
        self.proc = proc
        self.proxyname = args[0]
        self.argv = argv
        print self.env.drv.pool

def heartbeat(env, proc, args, argv):
    import time
    env.logger.info("Zabbix heartbeat daemon started %s"%repr(args))
    hb = Heartbeat(env, proc, args, argv)
    while True:
        time.sleep(5)
        env.logger.info("Heartbeat running")
        proc.setproctitle("Dummy daemon at: %s"%time.asctime())
