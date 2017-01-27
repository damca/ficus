#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys

class FigureManager(object):

    def __init__(self, filename=None, show=False, dpi=300,
                 nrows=1, ncols=1, tight_layout_rect=None,
                 figsize=None, gridspec_kw={}, subplot_kw={}):
        """Context manager for Matplotlib Figures.

        Parameters
        ----------
        filename : str
            if present, will save the file
        show : bool
        dpi : int
            SAVES with this dpi, does not create figure at this dpi
        nrows : int
        ncols : int
        tight_layout_rect : [float, float, float, float]
            The [0, 0, 1, 1] rectangle gives default plt.tight_layout behavior
            In Figure coordinates
        figsize: (num, num)
            None will grab rcParams default
        gridspec_kw : dict
            {'left': 0.15, 'right': ...}
        subplot_kw : dict
            {1 : {'sharex': 0, 'sharey': 0}, ..., }
            Keys are axis numbers (from left to right, top to bottom). Values
            are dicts specifying share axes. Higher ax numbers must share with
            lower ax numbers.

            Integers are replaced with axes.


        Returns
        ------
        """

        if not figsize:
            figsize = plt.rcParams['figure.figsize']
        cur_max = max(plt.get_fignums() or [0]) + 1
        self.fig = plt.figure(cur_max, figsize=figsize)
        print("Making Figure {}".format(cur_max))
        self.gs = GridSpec(nrows, ncols, **gridspec_kw)
        self.ax = []
        for ix, sp in enumerate(self.gs):
            if ix in subplot_kw:
                sub_kws = subplot_kw[ix]
                for key in sub_kws:
                    axnum = sub_kws[key]
                    sub_kws[key] = self.ax[axnum]
            else:
                sub_kws = {}
            self.ax.append( self.fig.add_subplot(sp, **sub_kws) )
        if len(self.ax) == 1:
            self.ax = self.ax[0]
        if tight_layout_rect is not None:
            self.gs.tight_layout(self.fig, rect=tight_layout_rect)

        self.dpi = dpi
        self.filename = filename
        self.show = show

        if self.fig != plt.gcf():
            self.clear()
            raise RuntimeError('Figure does not match active mpl figure')

    def __enter__(self):
        return self.fig, self.ax

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            if self.filename is not None:
                self.fig.savefig(self.filename, dpi=self.dpi)

            if self.show:
                plt.show(self.fig.number)
            self.clear()
        else:
            self.clear()
            return False

    def clear(self):
        plt.close(self.fig)
        del self.ax
        del self.fig
