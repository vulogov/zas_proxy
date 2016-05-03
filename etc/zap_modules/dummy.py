__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

##
## This is an example of the "daemon process"
## env - ZAP environment
## args, argv - arguments and keywork adruments passed
##
def daemon(env, args, argv):
    import time
    env.logger.info("Dummy daemon started")
    while True:
        time.sleep(5)
        env.logger.info("Dummy daemon running")


def main(env, logger, *args, **argv):
    args = tuple(list(args[2:]))
    logger.info("This startup function doesn't do much %s %s"%(repr(env),repr(args)))
