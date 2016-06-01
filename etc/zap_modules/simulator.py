__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from Process import *
from CLP import *

def item_simulator(env, proc, args, argv):
    proc.setproctitle("Item Simulator: %s" % repr(argv))

def simulator_controller(env, proc, args, argv):
    import time
    env.logger.info("Simulator controller daemon started %s"%repr(args))
    drv = env.cache_link("metrics")
    print drv.args
    while True:
        time.sleep(5)
        proc.setproctitle("Simulator Controller daemon at: %s" % time.asctime())