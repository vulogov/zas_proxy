import clips as _cm
import sys as _sys
import string as _string
import readline


class Shell(object):
    """an interactive CLIPS shell"""

    def __init__(self, env):
        self.__ps1 = "ZAS[%(cmdno)s/%(lineno)s]> "
        self.__ps2 = "ZAS[%(cmdno)s/%(lineno)s]: "
        self.__cmdno = 1
        self.__lineno = 1
        self.env = env
        readline.set_history_length(1000)

    def __cmdcomplete(self, cms):
        """check if CLIPS command is complete (stolen from 'commline.c')"""

        def eat_ws(s, i):
            """eat up whitespace"""
            while i < len(s) and s[i] in _string.whitespace: i += 1
            return i

        def eat_string(s, i):
            """eat up strings"""
            if s[i] != '"' or i >= len(s): return i
            i += 1
            while i < len(s):
                if s[i] == '"':
                    return i + 1
                else:
                    if s[i] == '\\': i += 1
                    i += 1
            if i > len(s): raise ValueError, "non-terminated string"
            return i

        def eat_comment(s, i):
            """eat up comments"""
            if s[i] != ';' or i >= len(s): return i
            while i < len(s) and s[i] not in '\n\r': i += 1
            return i + 1

        s = cms.strip()
        if len(s) == 0: return False
        depth = 0
        i = 0
        while i < len(s):
            c = s[i]
            if c in '\n\r' and depth == 0:
                return True
            elif c == '"':
                i = eat_string(s, i)
            elif c == ';':
                i = eat_comment(s, i)
            elif c == '(':
                depth += 1; i += 1
            elif c == ')':
                depth -= 1; i += 1
            elif c in _string.whitespace:
                i = eat_ws(s, i)
            else:
                i += 1
            if depth < 0: raise ValueError, "invalid command"
        if depth == 0:
            return True
        else:
            return False

    def Run(self):
        """start or resume an interactive CLIPS shell"""
        print "You are in ZAS(CLIPS) Shell. Type Ctrl-D or (exit) for quit."
        exitflag = False
        while not exitflag:
            self.__lineno = 1
            s = ""
            dic = {'cmdno': self.__cmdno, 'lineno': self.__lineno}
            prompt = self.__ps1 % dic
            try:
                while not self.__cmdcomplete(s):
                    if s: s += " "
                    s += raw_input(prompt).strip()
                    self.__lineno += 1
                    dic = {'cmdno': self.__cmdno, 'lineno': self.__lineno}
                    prompt = self.__ps2 % dic
            except ValueError, e:
                _sys.stderr.write("[ZAS SHELL] %s\n" % str(e))
            except EOFError:
                _cm.ErrorStream.Read()
                exitflag = True
            if s == "(exit)":
                exitflag = True
                break
            try:
                if not exitflag:
                    self.env.pc.clips.SendCommand(s, True)
            except _cm.ClipsError, e:
                _sys.stderr.write("[PYCLIPS] %s\n" % str(e))
            self.__cmdno += 1
            r0 = _cm.StdoutStream.Read()
            r1 = _cm.DisplayStream.Read()
            tx = _cm.TraceStream.Read()
            r = ""
            if r0: r += r0
            if r1: r += r1
            t = _cm.ErrorStream.Read()
            if r: r = "%s\n" % r.rstrip()
            if t: t = "%s\n" % t.rstrip()
            if tx: t = "%s\n" % tx.rstrip() + t
            if t: _sys.stderr.write(t)
            if r: _sys.stdout.write(r)
