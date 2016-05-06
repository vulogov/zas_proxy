__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from Process import

def heartbeat(env, proc, args, argv):
    import time
    env.logger.info("Zabbix heartbeat daemon started %s"%repr(args))
    #hb = Heartbeat(env, proc, args, argv)
    while True:
        time.sleep(5)
        env.logger.info("Heartbeat running")
        proc.setproctitle("Dummy daemon at: %s"%time.asctime())
