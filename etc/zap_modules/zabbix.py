__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from Process import *

def heartbeat(env, proc, args, argv):
    import time
    env.logger.info("Zabbix heartbeat daemon started %s"%repr(args))
    try:
        beat =  float(env.cfg("heartbeat", "beat"))
    except:
        beat = 1.0
    env.logger.info("Will send a heartbeat every %d seconds" %beat)
    drv = env.drv.driver("zabbix_active_proxy").driver()
    drv.build_chain()
    print repr(drv.toChain("host heartbeat"))
    while True:
        time.sleep(beat)
        env.logger.info("Heartbeat running")
        proc.setproctitle("Heartbeat daemon at: %s"%time.asctime())
        for m in env.pc.filter(relation="zabbix_server"):
            name = m.Slots["name"]
            port = m.Slots["port"]
            ip   = m.Slots["address"]
            print name, port, ip
