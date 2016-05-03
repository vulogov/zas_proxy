__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

def main(env, logger, *args, **argv):
    logger.info("This driver executed during startup and doesn't do much %s %s"%(repr(env),repr(args)))
    return True

