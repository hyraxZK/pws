#!/usr/bin/python

import math
import matplotlib as mplib
import matplotlib.pyplot as plt
import getopt
import sys

class Options(object):
    files = []
    legends = []

    plottype = 0
    ylabels = ["proof size, kiB", "prover time, seconds", "verifier time, seconds", "max memory usage, kiB", "time, seconds"]

    legendloc = 3
    loglin = "xy"
    plotfn = staticmethod(plt.loglog)

    axis = [None, None, None, None]
    xticks = None
    yticks = None

    filename = "out.pdf"

    hugemarkerstyles = "oh*<>sd"
    hugemarkercolors = ["green", "lightgreen", "blue", "cyan", "magenta", "red", "orange"]

    markerstyles = "o*<>sd"
    markercolors = ["green", "blue", "cyan", "magenta", "red", "orange"]

    mercompmarkerstyles = "ho^"
    mercompmarkercolors = ["lightgreen", "green", "teal"]

    markersize = 12

    huge_legend = False
    invert_z = False

    @classmethod
    def huge_style(cls):
        cls.markerstyles = cls.hugemarkerstyles
        cls.markercolors = cls.hugemarkercolors

    @classmethod
    def logarg_style(cls):
        cls.markerstyles = cls.hugemarkerstyles[1:]
        cls.markercolors = cls.hugemarkercolors[1:]

    @classmethod
    def mercomp_style(cls):
        cls.markerstyles = cls.mercompmarkerstyles
        cls.markercolors = cls.mercompmarkercolors
        cls.markersize = [12, 16, 16]

def make_plots():
    mplib.rc('text', usetex=True)
    mplib.rc('font', size=24)
    mplib.rc('text.latex', preamble='\usepackage{mathrsfs},\usepackage[cm]{sfmath},\usepackage{nicefrac}')

    results = [ process_file(f) for f in Options.files ]
    xaxes = []
    yaxes = []
    label = None
    for (lab, res) in results:
        if label is None:
            label = lab
        else:
            assert lab == label, "got unexpected label %s, expected %s" % (lab, label)
        xax = []
        yax = []
        yax2 = []
        for val in res:
            xax.append(val[0])
            if Options.plottype < 4:
                yax.append(val[1+Options.plottype])
            else:
                yax.append(val[2])
                yax2.append(val[3])
        xaxes.append(xax)
        yaxes.append((yax,yax2))

    def doplot(xaxis, yaxis, mstyle, mcolor, llabel, zord, msize):
        if Options.plottype == 4:
            pass
        elif Options.invert_z:
            zord = 8 + zord
        else:
            zord = 8 - zord
        Options.plotfn(xaxis, yaxis, color='black', linestyle='solid', marker=mstyle, markerfacecolor=mcolor, label=llabel, markersize=msize , zorder=zord)

    plt.cla()
    if Options.huge_legend:
        fig = plt.figure(figsize=(24,15))
    else:
        fig = plt.figure(figsize=(7,5))
    ax = plt.gca()
    plt.grid(True)

    for (idx, (xax, (yax,yax2))) in enumerate(zip(xaxes, yaxes)):
        leg = Options.legends[idx] if Options.legends is not None else None
        msize = Options.markersize
        if isinstance(msize,list):
            msize = Options.markersize[idx]

        if Options.plottype < 4:
            doplot(xax, yax, Options.markerstyles[idx], Options.markercolors[idx], leg, idx, msize)
        else:
            leg1 = "$\mathcal{P}$ time"
            leg2 = "$\mathcal{V}$ time"
            if leg is not None:
                leg1 = leg + " (" + leg1 + ")"
                leg2 = leg + " (" + leg2 + ")"
            doplot(xax, yax, Options.markerstyles[4], Options.markercolors[4], leg1, 2*idx, msize)
            doplot(xax, yax2, Options.markerstyles[1], Options.markercolors[1], leg2, 2*idx+1, msize)

    if all([ a is not None for a in Options.axis ]):
        plt.axis(Options.axis)

    #fig.canvas.draw_idle()
    if Options.xticks is not None:
        ax.set_xticks([], minor=True)
        ax.set_xticks(Options.xticks, minor=False)
        ax.set_xticklabels([ "$10^%d$" % int(math.log10(x)) if x>100 and x == 10 ** math.log10(x) else str(x) if x < 1 else str(int(x)) for x in Options.xticks ])
        ax.set_xticklabels([], minor=True)
    if Options.yticks is not None:
        ax.set_yticks([], minor=True)
        ax.set_yticks(Options.yticks, minor=False)
        ax.set_yticklabels([ "$10^%d$" % int(math.log10(y)) if y>100 and y == 10 ** math.log10(y) else str(y) if y < 1 else str(int(y)) for y in Options.yticks ])
        ax.set_yticklabels([], minor=True)
    #fig.canvas.draw_idle()

    plt.xlabel(label)
    plt.ylabel(Options.ylabels[Options.plottype])
    if Options.legends is not None or Options.plottype == 4:
        if Options.huge_legend:
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=len(Options.legends), mode="expand", borderaxespad=0., fancybox=True)
        else:
            plt.legend(loc=Options.legendloc, fontsize=24, fancybox=True, framealpha=1)
    plt.savefig(Options.filename, dpi=600, bbox_inches='tight')
    plt.close('all')

def process_file(filename):
    try:
        with open(filename, 'r') as fh:
            xlabel = fh.readline().strip()
            retvals = []
            procs = [int, lambda x: 24 * int(x) / 1024.0, float, float, int]
            for line in fh:
                retvals.append([ f(x) for (f, x) in zip(procs, line.strip().split(' ')) ])
                assert len(retvals[-1]) == 5
        return (xlabel, retvals)
    except IOError as err:
        print "Cannot open file %s: %s" % (filename, str(err))
        sys.exit(-1)

if __name__ == "__main__":
    uStr = "Usage: %s [-H] [-x <xlo,xhi>] [-y <ylo,yhi>] [-l <x|X><y|Y>] [-t {0,1,2,3}]\n               [-f <file1> [-f <file2> [...]]] [-L <legend1> [-L <legend2> [...]]]\n\nFor -l, X means linear x-axis, x means log, e.g., '-l Xy' means linear x, log y\n\nFor -t, 0=size, 1=ptime, 2=vtime, 3=mem, 4=ptime&vtime\n" % sys.argv[0]
    oStr = "x:y:X:Y:l:f:L:t:g:o:HGMm:Z"
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], oStr)
        if len(args) > 0:
            print uStr
            print "ERROR: extraneous arguments: %s" % args
            sys.exit(1)

        for (opt, arg) in opts:
            if opt == "-x":
                (Options.axis[0], Options.axis[1]) = [ float(s) for s in arg.split(',') ]
            elif opt == "-y":
                (Options.axis[2], Options.axis[3]) = [ float(s) for s in arg.split(',') ]
            elif opt == "-X":
                Options.xticks = [ float(s) for s in arg.split(',') ]
            elif opt == "-Y":
                Options.yticks = [ float(s) for s in arg.split(',') ]
            elif opt == '-l':
                Options.loglin = arg
            elif opt == '-f':
                Options.files.append(arg)
            elif opt == '-L':
                Options.legends.append(arg)
            elif opt == '-t':
                Options.plottype = int(arg)
            elif opt == "-g":
                Options.legendloc = int(arg)
            elif opt == "-o":
                Options.filename = arg
            elif opt == "-H":
                Options.huge_legend = True
                Options.huge_style()
            elif opt == "-G":
                Options.logarg_style()
            elif opt == "-M":
                Options.mercomp_style()
            elif opt == "-m":
                Options.markersize = int(arg)
            elif opt == "-Z":
                Options.invert_z = True
            else:
                assert False, "Logic error: got unexpected option %s from getopt" % opt

        if len(Options.loglin) != 2 or Options.loglin.lower() != "xy":
            raise ValueError("-l takes [xX][yY] (i.e., xy, XY, xY, or Xy)")
        elif Options.loglin == "xY":
            Options.plotfn = staticmethod(plt.semilogx)
        elif Options.loglin == "Xy":
            Options.plotfn = staticmethod(plt.semilogy)
        elif Options.loglin == "XY":
            Options.plotfn = staticmethod(plt.plot)
        else:
            Options.plotfn = staticmethod(plt.loglog)

        if len(Options.files) < len(Options.legends):
            raise ValueError("You must supply at least as many filenames as legend keys")
        elif len(Options.legends) < len(Options.files):
            Options.legends = None

        if Options.plottype > 4 or Options.plottype < 0:
            raise ValueError("-t must be 0, 1, 2, 3, or 4")

        if len(Options.files) == 0:
            raise ValueError("You must supply at least one file to plot!")

    except (ValueError, getopt.GetoptError) as err:
        print uStr
        print str(err)
        sys.exit(1)

    make_plots()
