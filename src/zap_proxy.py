#!/usr/bin/env python

##
## Zabbix Application Proxy (ZAP) main executable and source file
##
##

__author__ = 'Vladimir Ulogov'
__version__ = 'ZAP 0.0.1'

import logging
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
import multiprocessing
from multiprocessing.reduction import reduce_handle
from multiprocessing.reduction import rebuild_handle
import setproctitle


logger = logging.getLogger("ZAP")
ARGS = None
ENV  = None


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

class ZAPEnv:
    def __init__(self, args):
        self.args = args


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
    logger.info("Entering loop...")
    while True:
        pass


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
    ENV = ZAPEnv(args)
    Main(args, parser)


if __name__ == '__main__':
    main()


