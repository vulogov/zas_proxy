__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from Process import *
from TCP import TCPClient

def heartbeat(env, proc, args, argv):
    import time
    env.logger.info("Zabbix heartbeat daemon started %s"%repr(args))

    beat =  env.cfg("heartbeat", "beat", float, 1.0)
    bufsize = env.cfg("client", "bufsize", int, 4096)
    timeout = env.cfg("client", "timeout", float, 3.0)
    env.logger.info("Will send a heartbeat every %d seconds" %beat)
    drv = env.drv.driver("zabbix_active_proxy").driver()
    drv.set_drv_context()
    drv.build_chain()
    while True:
        time.sleep(beat)
        env.logger.info("Heartbeat running")
        proc.setproctitle("Heartbeat daemon at: %s"%time.asctime())
        for m in env.pc.filter(relation="zabbix_server"):
            name = m.Slots["name"]
            port = m.Slots["port"]
            ip   = m.Slots["address"]
            hostname = m.Slots["hostname"]
            drv.update_ctx_in_chain(host=hostname)
            heartbeat = str(drv.toChain("proxy heartbeat"))
            print repr(heartbeat)
            print name, port, ip
            s = TCPClient(ip, port, timeout)
            s.bufsize = bufsize
            s.write(heartbeat)
            buf = s.read()
            print drv.fromChain(buf)

