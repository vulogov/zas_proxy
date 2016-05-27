__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

##
## This is an example of the "daemon process"
## env - ZAP environment
## args, argv - arguments and keywork adruments passed
##
def daemon(env, proc, args, argv):
    import time
    env.logger.info("Dummy daemon started %s"%repr(args))
    while True:
        time.sleep(500)
        env.logger.info("Dummy daemon running")
        proc.setproctitle("Dummy daemon at: %s"%time.asctime())


def main(env, logger, *args, **argv):
    #args = tuple(list(args[2:]))
    logger.info("This startup function doesn't do much %s"%repr(args))
