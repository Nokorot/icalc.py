
import numpy as np

import functools, operator

maths_expr = """abs,acos:arccos,asin:arcsin,atan:arctan,atan2:arctan2,ceil,cos,
cosh,degrees,exp,fabs,floor,fmod,frexp,hypot,ldexp,log,log10,modf,radians,sin,
sinh,sqrt,tan,tanh""".replace("\n", "").split(",")

def pair(k):
    if ':' in k: [key, value] = k.split(':')
    else:        [key, value] = [k,k]
    return (key, np.__dict__[value]);
basic_np_fns = dict([pair(k) for k in maths_expr]);

def sum_cmd(*args):
    return sum(args)

def prod_cmd(*args):
    return functools.reduce(operator.mul, args)

def avg_cmd(*args):
    return sum(args)/len(args)


# This should probably not be here
def as_fn(state, args):
    if len(args) < 1: 
        print("Err: Too few arguments.\nUsage: ´as <name>´")
        return 

    val = state.top() if len(args) == 1 else state.eval("".join(args[1:]))
    state.set_var(args[0], val)


module = { 
    "funcs":  basic_np_fns | { 
        "sum": sum_cmd,
        "avg": avg_cmd,
        "prod": prod_cmd,
    },
    "lazy_fns": {
        "as":  as_fn,
    },
    "vars": {
        "pi": np.pi,
        "e": np.e,
    }
}
