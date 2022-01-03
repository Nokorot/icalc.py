
# from sympy import *
# import pyplot 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

title = None;
line_style = [];
ranges = {};
N = 501;

# def set(args):
#     def setTitle(args):
#         global title
#         title = ' '.join(args[0])
#     def setLineStyle(args):
#         ls = json.loads(args[0])
#         lw = ls.get('linewidth', []);
#         lc = ls.get('linecolor', []);
#         dt = ls.get('dashtype', []);
# 
#         global line_style;
#         line_style = []
#         for i in range(max(len(lw), len(lc), len(dt))):
#             ls = {}
#             if i < len(lc): ls['color']     = lc[i].replace('\'', '');
#             if i < len(lw): ls['linewidth'] = int(lw[i]);
#             else: ls['linewidth'] = 2;
#             if i < len(dt): ls['linestyle'] = dt[i];
#             line_style.append(ls);
#     def setRanges(args):
#         global ranges;
#         ranges = json.loads(args[0]);
# 
#     cmd = {
#         'output':       None,
#         'title':        setTitle,
#         'linestyle':    setLineStyle,
#         'ranges':       setRanges
#     }.get(args[0], None);
#     if cmd != None: cmd(args[1:]);
 
def xrange(min, max):
    ranges["xrange"] = (min, max)

def yrange(min, max):
    ranges["yrange"] = (min, max)

def make_fig():
    dpi = 70;
    plt.figure(figsize=(800/dpi, 600/dpi), dpi=dpi)
    plt.title(title, fontname='Helvetica')

def plot(state, args):
    exprs = ' '.join(args).split(',');

    make_fig()
    x = np.linspace(*ranges.get('xrange', (-1,1)), N);
 
    for (i, exp) in enumerate(exprs):
        ls = line_style[i] if i < len(line_style) else {};
        plt.plot(x, state.eval(exp, {'x': x}), **ls);
    
    plt.show()
    # plt.savefig('tmp/plot.png');

def splot(state, args):
    exprs = ' '.join(args).split(',');

    make_fig()
    ax = plt.axes(projection='3d')

    x = np.linspace(*ranges.get('xrange', (-1,1)), N);
    y = np.linspace(*ranges.get('yrange', (-1,1)), N);
    x, y = np.meshgrid(x,y)

    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(x,y);

    for (i, exp) in enumerate(exprs):
        ls = line_style[i] if i < len(line_style) else {};
        ax.plot_surface(x, y, state.eval(exp, {'x': x, 'y':y, 'r':r, 'theta':theta}), cmap='viridis');

    plt.show()
    # plt.savefig('tmp/splot.png');

def implot(state, args):
    exprs = ' '.join(args).split(',');
    
    make_fig()
 
    x = np.linspace(*ranges.get('xrange', (-1,1)), N);
    y = np.linspace(*ranges.get('yrange', (-1,1)), N);
    x, y = np.meshgrid(x,y)

    # r = np.sqrt(x**2 + y**2)
    # theta = np.arctan2(x,y);

    plt.axis('equal')

    for (i, exp) in enumerate(exprs):
        ls = line_style[i] if i < len(line_style) else {};
        ls = dict([(k+'s',v) for (k,v) in ls.items()]);
        plt.contour(x,y, state.eval(exp.replace('=','-',1), {'x': x, 'y':y}), [0], **ls);
    
    plt.show()
    # plt.savefig('tmp/implot.png');

module = { 
        # Idea:
    # "docs": {
    #     "plot": "This function plots a graph"
    # }

    "funcs": {
        "xrange": xrange,
        "yrange": yrange,
    },
    "lazy_fns": {
        "plot":   plot,
        "splot":  splot,
        "implot": implot,
    },
}
