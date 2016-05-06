__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import multiprocessing
import setproctitle
from Object import Object

def proctitle(main, msg, proc="ZAP"):
    setproctitle.setproctitle("%s(%s): %s"%(proc, main, msg))

def daemon_process(env, name, main, proc, args, argv):
    if not name:
        env.logger.info("Can not execute process without a name")
        return
    if not main:
        env.logger.info("Can not execute process without a main function")
        return
    env.logger.info("Attempting to execute %s as %s"%(main, name))
    proctitle(main, name)
    try:
        env.pc(main, env, proc, args, argv)
    #except ValueError, msg:
    except FloatingPointError, msg:
        env.logger.error("Exception in %s: %s"%(main, msg))

class DaemonProcess(multiprocessing.Process, Object):
    def __init__(self, **argv):
        self.Object__set_attr("main", argv)
        self.Object__set_attr("name", argv)
        self.Object__set_attr("env", argv)
        self.Object__set_attr("target", argv)
        self.Object__set_attr("args", argv, ())
        self.Object__set_attr("kw", argv, {})
        passed_args = (self.env, self.name, self.main, self, self.args, self.kw)
        multiprocessing.Process.__init__(self, target=self.target, name=self.name, args=passed_args)
        self.Object__set_attr("daemon", argv, True)
        self.authkey=self.env.authkey
        self.Initialize()
    def setproctitle(self, msg):
        proctitle(self.main, msg)
