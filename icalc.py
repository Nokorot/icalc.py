#!/usr/bin/python3.9

import cmd, sys, os
import re
# TODO: A command to store a variable permanently ie. to disk

VERSION = '0.1'

# Linux: 
# TODO: using ~ is less reliable then $HOME
MOD_DIR = [ f"{os.environ.get('HOME')}/.local/share/icalc/mods/", "mods" ]
sys.path.extend(MOD_DIR)

def valid_name(arg):
    return arg.isalpha()

# This does not realy work
def __path_import__(name, path, *args):
    import_paths, sys.path = sys.path, path
    m = __import__(name, *args)
    sys.path = import_paths
    return m

class State:
    vars = {}
    funcs = {}
    lazy_fns = {}

    hist = []

    def import_mod(self, name):
        mod = __import__("%s_mod" % name)

        if not "module" in mod.__dict__:
            print("Err: This is not a module")
        
        for (key, value) in mod.module.items():
            if key in ["lazy_fns", "funcs", "vars"]:
                exec("self.%s |= value" % key)

    def set_var(self, name, val):
        if not valid_name(name):        # TODO: check if name is some default func
            print("Err: '%s' is not a valid variable name.\n" % name) 
            return

        self.vars[name] = val

    def top(self):
        return self.hist[-1]

    def new(self, val):
        if val is None: return 
        if len(self.hist) > 0 and val == self.hist[-1]: 
            return len(self.hist)-1, val
        self.hist.append(val)
        self.vars["_"] = val
        return len(self.hist)-1, val

    def drop(self):
        if len(self.hist) == 0: return
        self.hist.pop()
        if len(self.hist) == 0: return

        val = self.hist[-1]
        self.vars["_"] = val
        return len(self.hist)-1, val

    def eval(self, expr, locals={}):
        globals = self.funcs | self.vars

        xs = re.findall("![0-9]+", expr)
        for x in xs:
            v = str(self.hist[int(x[1:])])
            print("'%s' '%s'" % (x, v))
            expr = expr.replace(x, v)
            print(expr)

        return eval(expr, globals, locals)

    def exec(self, line):
        words = re.split("\s+", line)
        # This might be interesting if we want some lasy eval
        if words[0] in self.lazy_fns:
            return self.new( self.lazy_fns[words[0]](self, words[1:]) )

        if words[0] in self.funcs:
            args = (self.eval(arg) for arg in words[1:])
            return self.new( self.funcs[words[0]]( *args ) )


        return self.new( self.eval(line) )

class ICalc(cmd.Cmd):
    intro = "ICalc - Basic Calc! \n Type help or ? to list commands."
    prompt = "> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.state = State()
        self.state.import_mod("basics")


    def default(self, line):
        try:
            res = self.state.exec(line)
            if res is None: return

            print("!%d -> " % res[0], res[1])
        except Exception as e:
            print(e)
 
    def do_use(self, arg):
        self.state.import_mod(arg)

    def do_list(self, arg): 
        # TODO: This needs some work
        if arg == "funcs":
            for (k,v) in self.state.funcs.items():
                print(k)
        if arg == "":
            for (k,v) in self.state.vars.items():
                print(k, v)

    def do_drop(self, arg):
        # TODO: This needs some work
        print( self.state.drop() )

    def do_hist(self, arg):
        # TODO: This needs some work
        print( " == ", self.state.hist)

    def do_exit(self, arg):
        return self.close()
    
    def do_quit(self, arg):
        return self.close()

    def close(self):
        return True

import argparse

class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)


if __name__ == "__main__":
    # os.system("mkfifo /tmp/icalc-socket")
    # for arg in sys.argv[1]:
    #     if arg == "-d":
    #         f = open("/tmp/icalc-socket", r)
    #         sys.stdin == f

    
    parser = argparse.ArgumentParser(add_help=False, formatter_class=CapitalisedHelpFormatter)
    parser._positionals.title = 'Positional arguments'
    parser._optionals.title = 'Optional arguments'
    parser.add_argument('-v', '--version', action='version',
                        version=f"%(prog)s {VERSION}", help="Show program's version number and exit.")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    # parser.add_argument('-c', action='help',
    #                     help='Show this help message and exit.')

    parser.parse_args()

    ICalc().cmdloop()

    # f.close()
