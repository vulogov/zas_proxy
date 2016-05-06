#!/usr/bin/env python

##
## Zabbix Application Proxy (ZAP) main executable and source file
##
##

__author__ = 'Vladimir Ulogov'
__version__ = 'ZAP 0.0.1'
__proc__    = 'ZAP'

import logging
import setproctitle
import imp
import types
import argparse
import clips
import sys
import os
import time
import signal
import daemonize
import SocketServer
import Queue
import socket
import uuid
import multiprocessing
from multiprocessing.reduction import reduce_handle
from multiprocessing.reduction import rebuild_handle



logger = logging.getLogger("ZAP")
ARGS = None
ENV  = None

########################################################################################################################
## Service fuctions
########################################################################################################################
def check_file(fname, mode):
    fname = os.path.expandvars(fname)
    if os.path.exists(fname) and os.path.isfile(fname) and os.access(fname, mode):
        return True
    return False

def check_directory(dname):
    dname = os.path.expandvars(dname)
    if os.path.exists(dname) and os.path.isdir(dname) and os.access(dname, os.R_OK):
        return True
    return False

def check_file_read(fname):
    return check_file(fname, os.R_OK)

def Is_Process_Running():
    global ARGS, logger

    try:
        pid = int(open(ARGS.pid).read())
    except:
        logger.error("Can not detect ZAP process ID from %s" % ARGS.pid)
        return None
    if not os.path.exists('/proc/%d' % pid):
        logger.info("ZAP process with PID=%d isn't running. Removing stale PID file" % pid)
        os.unlink(args.pid)
        return None
    return pid

def check_module(fname):
    if not check_file_read(fname):
        return False
    if os.path.getsize(fname) > 0:
        return True
    return False

def check_file_write(fname):
    return check_file(fname, os.W_OK)

def check_file_exec(fname):
    return check_file(fname, os.X_OK)

def get_dir_content(dname):
    if not check_directory(dname):
        return []
    ret = []
    for f in os.listdir(dname):
        if not check_file_read("%s/%s"%(dname, f)):
            continue
        ret.append((f, "%s/%s"%(dname, f), os.path.splitext(f)))
    return ret

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring


class Object(object):
    def Object__set_attr(self, key, argv, default=None):
        if argv.has_key(key):
            setattr(self, key, argv[key])
        else:
            setattr(self, key, default)


########################################################################################################################
## Process-related classes
########################################################################################################################


#class DaemonProcess(multiprocessing.Process, Object):
#    def __init__(self, **argv):
#        self.Object__set_attr("main", argv)
#        self.Object__set_attr("name", argv)
#        self.Object__set_attr("env", argv)
#        self.Object__set_attr("args", argv, ())
#        self.Object__set_attr("kw", argv, {})
#        passed_args = (self.env, self.name, self.main, self, self.args, self.kw)
#        multiprocessing.Process.__init__(self, target=daemon_process, name=self.name, args=passed_args)
#        self.authkey=self.env.authkey
#        self.daemon = True
#    def setproctitle(self, msg):
#        proctitle(self.main, msg)

def listener_process(env, name, driver, proc, args, kw):
    if not driver:
        env.logger.info("Can not execute listener process without a driver")
        return
    if not name:
        env.logger.info("Can not execute listener process without a name")
        return
    return




########################################################################################################################
## Network-related classes
########################################################################################################################



class ZAPConnectionWorker(multiprocessing.Process):
    def __init__(self, sq):

        self.SLEEP_INTERVAL = 1  # base class initialization
        multiprocessing.Process.__init__(self)
        self.socket_queue = sq
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            try:
                h = self.socket_queue.get_nowait()
                fd = rebuild_handle(h)
                client_socket = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
                received = client_socket.recv(1024)
                print "Recieved on client: ", received
                client_socket.close()
            except Queue.Empty:
                pass
            time.sleep(self.SLEEP_INTERVAL)


class ZAPTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        h = reduce_handle(self.request.fileno())
        socket_queue.put(h)




########################################################################################################################
## Clips and Clips
########################################################################################################################


def clp2py(val):
    try:
        t,v = val.clrepr()
    except:
        return val
    if t in [0,1,3]:
        return v
    elif t == 2 and v == 'TRUE':
        return True
    elif t == 2 and v == 'FALSE':
        return False
    return v

def multifield2py(val):
    out = []
    for f in val:
        out.append(clp2py(f))
    return tuple(out)

class FACT:
    def facts(self, fname):
        self.clips.LoadFacts(fname)
    def load_facts(self, **args):
        return self._load(self.clips.LoadFacts, self.clips.LoadFactsFromString, args)

class LOADER:
    def _load(self, lf_file, lf_string, args):
        if args.has_key("file") and lf_file:
            if not check_module(args["file"]):
                raise IOError, "File %s not found or not accessible"%args["file"]
            return apply(lf_file, (args["file"],))
        elif args.has_key("data") and len(args["data"]) and lf_string:
            return apply(lf_string, (args["data"],))
        else:
            raise ValueError, "Loader requested to load not from file, nether from string"

class CLPEXEC:
    def load(self, **args):
        return self._load(self.clips.Load, self.clips.Eval, args)
    def execute(self, **args):
        return self._load(self.clips.BatchStar, self.clips.Eval, args)

class CLP(Object, LOADER, FACT, CLPEXEC):
    def __init__(self, **argv):
        self.argv = argv
        self.clips = clips.Environment()
        self.clear()
    def clear(self):
        self.clips.Clear()
        self.clips.Reset()
    def current(self):
        self.clips.SetCurrent()


########################################################################################################################
## Python and Python
########################################################################################################################

class PYLOADER:
    def __init__(self):
        self.mods = {}
    def module_loaded(self, mod, fun):
        pass
    def mod_exec(self, _mod):
        if type(_mod) == types.StringType:
            ## Passing the name
            _mod = self.find_the_mod(_mod)
            if _mod == None:
                return []
        elif type(_mod) == types.ModuleType:
            _mod = _mod
        else:
            return []
        out = []
        for f in dir(_mod):
            if type(getattr(_mod, f)) != types.FunctionType:
                continue
            out.append(f)
        return out
    def find_the_mod(self, mod_name):
        for p in self.mods.keys():
            if self.mods[p].has_key(mod_name):
                return self.mods[p][mod_name]
        return None
    def reload_mods(self, path=None):
        if not path:
            _path = self.path
        else:
            _path = path
        for p in _path:
            if not self.mods.has_key(p):
                self.mods[p] = {}
            dir = get_dir_content(p)
            for m in dir:
                file, full_path, mod = m
                modname, ext = mod
                if ext not in [".py",] or self.find_the_mod(modname) != None:
                    continue
                try:
                    _mod = imp.load_source(modname, full_path)
                except:
                    continue
                self.mods[p][modname] = _mod
                f_list = self.mod_exec(_mod)
                for f in f_list:
                    self.module_loaded(modname, f)
        for p in self.mods.keys():
            if p not in self.path:
                del self.mods[p]

class PYEXEC:
    def __call__(self, modname, *args, **kw):
        parse = modname.split(".")
        if len(parse) == 1:
            _mod     = modname
            _fun     = "main"
        elif len(parse) >= 2:
            _mod = parse[0]
            _fun = parse[1]
        else:
            raise ValueError, "Bad function name %s"%modname
        mod = self.find_the_mod(_mod)
        if mod == None:
            raise ValueError, "Module %s not found"%modname
        try:
            fun = getattr(mod, _fun)
        except:
            raise ValueError, "Function %s.%s not exists"%(_mod, _fun)
        try:
            return apply(fun, args, kw)
        except FloatingPointError:
        #except KeyboardInterrupt:
        #   return
        #except:
            raise ValueError, "Error in %s.%s"%(_mod, _fun)
    def execute(self, _fun, *args, **kw):
        out = {}
        for p in self.mods.keys():
            for m in self.mods[p].keys():
                mod = self.mods[p][m]
                try:
                    fun = getattr(mod, _fun)
                except:
                    continue
                try:
                    ret = apply(fun, args, kw)
                    out[m] = ret
                except:
                    continue
        return out

class PY(Object, PYLOADER, PYEXEC):
    def __init__(self, *path):
        self.path = []
        for d in list(path):
            if check_directory(d):
                self.path.append(d)
        PYLOADER.__init__(self)
        self.reload_mods()
    def __add__(self, path):
        if not check_directory(path) or path in self.path:
            return self
        self.path.append(path)
        return self
    def __sub__(self, path):
        if path in self.path:
           self.path.remove(path)
        return self

class PYCLP(PY,CLP):
    def __init__(self, **argv):
        self.argv = argv
        self.path = []
        if self.argv.has_key("path"):
            self.Object__set_attr("path", self.argv)
            apply(PY.__init__, tuple([self,] + [self.path,]))
        else:
            apply(PY.__init__, (self,))
        apply(CLP.__init__, (self,), argv)
    def load_pyclp_module(self, name):
        import fnmatch
        mod = self.find_the_mod(name)
        if mod == None:
            raise ValueError, "PYCLP module %s not found"%name
        c = 0
        for e in dir(mod):
            if fnmatch.fnmatch(e, "*_clips"):
                fun_name = rchop(e,"_clips")
                try:
                    fun = getattr(mod, fun_name)
                except:
                    continue
                clips.RegisterPythonFunction(fun)
                self.clips.Build(getattr(mod, e))
                c += 1
        return c
    def filter(self, **args):
        out = []
        for f in self.clips.FactList():
            if args.has_key("relation") and f.Relation == args["relation"]:
                out.append(f)
                continue
            for k in args.keys():
                if k == "relation":
                    continue
                if f.Slots.has_key(k) and f.Slots[k] == args[k]:
                    out.append(f)
        return out

########################################################################################################################
## Environment, Drivers, etc ...
########################################################################################################################


class DriverPool:
    def __init__(self):
        self.chain = {}
        self.pool = {}
        self.pool["startup"] = {}
        self.pool["cache"] = {}
        self.pool["db"] = {}
        self.pool["protocol"] = {}
    def register(self, drv_type, name, obj):
        self.pool[drv_type][name] = obj
    def register_chain(self, name, chain):
        self.chain[name] = chain
    def cache(self, name):
        return self.pool["cache"][name]
    def db(self, name):
        return self.pool["db"][name]
    def protocol(self, name):
        return self.pool["protocol"][name]
    def protocols(self):
        return self.pool["protocol"].keys()
    def driver(self, name):
        for p in self.pool.keys():
            if name in self.pool[p].keys():
                return self.pool[p][name]
        return None



class ZAPEnv:
    def __init__(self, args):
        global logger
        self.args = args
        self.logger = logger
        self.logger.info("Initializing environment")
        self.authkey = str(uuid.uuid4())
        self.pc = PYCLP()
        self.drivers = PYCLP()
        self.drv = DriverPool()
    def bootstrap(self):
        bootstrap_file = "%s/%s"%(self.args.config, self.args.bootstrap)
        configuration_file = "%s/%s"%(self.args.config, self.args.configuration)
        self.logger.info("Bootstrapping system with %s"%bootstrap_file)
        if not check_file_read(bootstrap_file):
            self.logger.error("File %s is not available for READ"%bootstrap_file)
            return False
        try:
            self.pc.load(file=bootstrap_file)
        except:
            return False
        self.logger.info("Configuring system with %s"%configuration_file)
        if not check_file_read(configuration_file):
            self.logger.error("File %s is not available for READ"%bootstrap_file)
            return False
        try:
            self.pc.facts(configuration_file)
        except:
            return False
        try:
            self.logger.info("Running the configuration")
            self.pc.clips.Run()
        except:
            self.logger.error("Error in running the configuration")
            return False
        for m in self.pc.filter(relation="application"):
            self.logger.info("ZAP Application name       : %-40s"%m.Slots["name"])
            self.logger.info("ZAP Application description: %-40s"%m.Slots["desc"])
            self.logger.info("ZAP Application POC        : %-40s"%m.Slots["poc"])
            self.logger.info("ZAP Application email      : %-40s"%m.Slots["email"])
            self.logger.info("ZAP Application phone      : %-40s"%m.Slots["phone"])
        self.set_pythonpath()
        for m in self.pc.filter(relation="py_module"):
            self.logger.info("Adding path %s for the '%s'"%(m.Slots["path"],m.Slots["name"]))
            if not m.Slots["path"]:
                self.logger.error("Path %s for Python modules is incorrect"%m.Slots["path"])
                continue
            self.pc += str(m.Slots["path"])
        self.pc.reload_mods()
        for m in self.pc.filter(relation="clips_mod"):
            self.logger.info("Loading CLP(%s) functions for '%s'"%(m.Slots["name"],m.Slots["desc"]))
            self.pc.load_pyclp_module(str(m.Slots["name"]))
        for m in self.pc.filter(relation="start"):
            try:
                self.pc(m.Slots["name"], self, self.logger, multifield2py(m.Slots["args"]))
            #except ValueError, msg:
            except ZeroDivisionError, msg:
                self.logger.error("Exception in startup module: %s"%msg)
        return True
    def set_pythonpath(self):
        for m in self.pc.filter(relation="pythonpath"):
            path = clp2py(m.Slots["path"])
            if not check_directory(path):
                self.logger.error("PYTHONPATH '%s' can not be accessed"%path)
                continue
            self.logger.info("PYTHONPATH: %s"%path)
            sys.path.append(path)

    def load_drivers(self):
        self.logger.info("Loading ZAP drivers")
        for m in self.pc.filter(relation="driver_path"):
            self.logger.info("Adding driver path %s for the '%s'"%(m.Slots["path"],m.Slots["name"]))
            if not m.Slots["path"]:
                self.logger.error("Path %s for ZAP drivers is incorrect"%m.Slots["path"])
                return False
            self.drivers += str(m.Slots["path"])
        self.drivers.reload_mods()
        self.logger.info("Registering drivers chains")
        for m in self.pc.filter(relation="driver"):
            driver_type = str(m.Slots["type"]).lower()
            try:
                obj = self.drivers("%s.main"%m.Slots["name"], self, self.logger, multifield2py(m.Slots["args"]))
            #except ValueError, msg:
            except FloatingPointError, msg:
                self.logger.error("Exception in initialisation: %s"%msg)
                return False
            self.drv.register(driver_type, str(m.Slots["name"]), obj)
        for m in self.pc.filter(relation="driver_chain"):
            name = str(m.Slots["name"]).strip()
            if not name:
                continue
            self.logger.info("Registering drivers chain for %s"%name)
            self.drv.register_chain(name, multifield2py(m.Slots["chain"]))
        return True
    def run_daemons(self):
        from Process import *
        self.logger.info("Starting background ZAP daemons")
        for m in self.pc.filter(relation="daemon"):
            self.logger.info("Attempting to spawn '%s' as %s"%(m.Slots["desc"], m.Slots["main"]))
            try:
                d = DaemonProcess(name=str(m.Slots["name"]), main=str(m.Slots["main"]), daemon=True, target=daemon_process, env=self, args=multifield2py(m.Slots["args"]))
                d.start()
            except ZeroDivisionError:
                self.logger.error("Exception while starting '%s' as %s"%(m.Slots["desc"], m.Slots["main"]))
    def start_listeners(self):
        self.logger.info("Starting network listeners")
        for m in self.pc.filter(relation="daemon"):
            print m
        return True





########################################################################################################################
## Main App functions
########################################################################################################################



def build_argparser():
    global ARGS
    parser = argparse.ArgumentParser(description='ZAP_proxy - Zabbix Application Proxy')
    parser.add_argument('--config', '-c', nargs='?', default=".", action="store",
                        help='Path to the configuration directory')
    parser.add_argument('--log', '-l', nargs='?', default="/tmp/zap_proxy.log", action="store",
                        help='Path to the Log file')
    parser.add_argument('--verbose', '-v', default=0, action="count", help='Verbosity level')
    parser.add_argument('--cmd', '-C', default="help", action="store",
                        help="Execute specific command. Possibilities are: [start|stop|restart|help]")
    parser.add_argument('--daemonize', '-d', default=False, action="store_true", help='Run ZAP as a Unix Daemon')
    parser.add_argument('--pid', '-P', default="/tmp/zap_proxy.pid", action="store", help='Path to the PID file')
    parser.add_argument('--user', '-U', default="zabbix", action="store", help='Run ZAP as User')
    parser.add_argument('--group', '-G', default="zabbix", action="store", help='Set Group privileges for a ZAP')
    parser.add_argument('--bootstrap', '-b', default="bootstrap.clp", action="store", help='Name of the ZAP bootstrap file')
    parser.add_argument('--configuration', '-f', default="configuration.clp", action="store", help='Name of the ZAP configuration file')
    ARGS = parser.parse_args()
    return parser, ARGS


def set_logging(args):
    global logger

    fmt = logging.Formatter("%(asctime)s  %(message)s", "%m-%d-%Y %H:%M:%S")

    if args.log == '-':
        f = logging.StreamHandler()
    else:
        f = logging.FileHandler(args.log)
    f.setFormatter(fmt)
    logger.addHandler(f)
    if args.verbose == 1:
        logger.setLevel(logging.CRITICAL)
    elif args.verbose == 2:
        logger.setLevel(logging.ERROR)
    elif args.verbose == 3:
        logger.setLevel(logging.WARNING)
    elif args.verbose == 4:
        logger.setLevel(logging.INFO)
    elif args.verbose == 5:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def Loop():
    global logger, ARGS

    ENV = ZAPEnv(ARGS)
    if not ENV.bootstrap():
        logger.error("Error in boostrapping and/or configuration")
        return
    if not ENV.load_drivers():
        logger.error("Error in loading ZAP drivers")
        return
    ENV.run_daemons()
    if not ENV.start_listeners():
        logger.error("Error in listeners initialization")
        return
    logger.info("Entering loop...")
    from Process import proctitle
    proctitle("main", "Main loop", __proc__)

    try:
        while True:
            time.sleep(5)
    except:
        logger.info("Exit loop...")
        childs = multiprocessing.active_children()
        for p in childs:
            logger.info("Terminating %s"%p.name)
            p.terminate()
            p.join()


def Start(args, parser):
    global logger

    import pwd, grp

    try:
        u = pwd.getpwnam(args.user)
        uid = u.pw_uid
        home = u.pw_dir
        gid = grp.getgrnam(args.group).gr_gid
    except KeyError:
        logger.error("User %(user)s or Group %(group)s does not exists" % args)
        return None
    daemon = daemonize.Daemonize(app="ZAP", pid=args.pid, action=Loop, chdir=home, user=args.user, group=args.group,
                                 logger=logger, foreground=not args.daemonize)
    logger.info("Executing ZAP as %s/%s in %s" % (args.user, args.group, home))
    daemon.start()
    return daemon





def Stop(args, parser):
    global logger

    logger.info("Trying to stop ZAP daemon")
    pid = Is_Process_Running()
    if not pid:
        logger.info("ZAP isn't running. Nothing to stop")
        return True
    for i in range(10):
        logger.info("Trying to TERM ZAP daemon. Appempt #%d" % i)
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        if not Is_Process_Running():
            logger.info("ZAP is Gone!")
            return True
    if Is_Process_Running():
        logger.error("ZAP process is still there. Killing it")
    for i in range(10):
        logger.info("Trying to TERM ZAP daemon. Appempt #%d" % i)
        os.kill(pid, signal.SIGHUP)
        time.sleep(5)
        if not Is_Process_Running():
            logger.info("ZAP is Gone!")
            return True
    if Is_Process_Running():
        logger.error("ZAP process is still there. Nothing is I can do. Please contact System Administrator.")
    return False


def Main(args, parser):
    global logger
    if args.cmd.lower() == 'help':
        parser.print_help()
    elif args.cmd.lower() == "start":
        Start(args, parser)
    elif args.cmd.lower() == "stop":
        Stop(args, parser)
    elif args.cmd.lower() == "restart":
        if not Stop(args, parser):
            logger.error("Can not stop ZAP process. Restart is failed")
            return
        Start(args, parser)
    else:
        parser.print_help()


def main():
    global logger, ENV
    parser, args = build_argparser()
    set_logging(args)
    logger.critical("Zabbix Application Proxy ver %s" % __version__)
    print args
    Main(args, parser)


if __name__ == '__main__':
    main()


