"""

"""

import pickle
import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from oap.core import decompress
from oap.bnp import progress, Runtime
from oap.__conf__ import COLUMN, ROSETTE


def load_imagefile(filename):
    with open(filename, "rb") as file:
        imagefile = pickle.load(file)
    return imagefile


class Imagefile:

    def __init__(self, filename=None,
                 timeframes=None, x_sizes=None, y_sizes=None,
                 exclude_buffers=None, include_buffers=None,
                 truncated=True, poisson=True, cluster=True, principal=True, status=True, buffer_id=False,
                 diodes=64, resolution=15):

        self.filename = filename
        self.diodes = diodes
        self.resolution = resolution

        # Private variables for plotting
        self.__n_figures = None
        self.__plt_iterator = None
        self.__fig = None
        self.__axes = None
        self.__auto_plot = None

        self.arrays = []
        if self.filename is not None:
            self.number_of_particles = decompress(self.filename,
                                                  arrays=self.arrays,
                                                  timeframes=timeframes,
                                                  x_sizes=x_sizes,
                                                  y_sizes=y_sizes,
                                                  exclude_buffers=exclude_buffers,
                                                  include_buffers=include_buffers,
                                                  truncated=truncated,
                                                  poisson=poisson,
                                                  cluster=cluster,
                                                  principal=principal,
                                                  status=status,
                                                  buffer_id=buffer_id)

    def __len__(self):
        return self.number_of_particles

    def __iter__(self):
        self.offset = 0
        return self

    def __next__(self):
        if self.offset == 0 or self.offset < self.number_of_particles:
            i = self.offset
            self.offset += 1
            return self.arrays[i]
        else:
            raise StopIteration

    def __add__(self, other):
        new = Imagefile()
        new.arrays = self.arrays
        new.arrays += other.arrays
        if self.arrays[0].second > other.arrays[0].second:
            new.arrays.sort(key=lambda x: x.second, reverse=True)
        return new

    def save(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    def classify(self, batch_size=1024):

        from oap.deep.classifier import ParticleClassifier

        runtime = Runtime().start()
        pc_c = ParticleClassifier(p_type=COLUMN)
        pc_r = ParticleClassifier(p_type=ROSETTE)
        arrays = self.get_arrays(x=(5, 64), y=(5, 64))
        iterations = len(arrays)//batch_size if len(arrays) % batch_size == 0 else len(arrays)//batch_size+1

        for i in range(iterations):
            progress(i, iterations, prefix="Classification ", suffix=" Complete")
            batch = [arrays[i*batch_size+j].tensor() for j in range(batch_size) if i*batch_size+j < len(arrays)]
            batch = np.reshape(batch, (len(batch), 64, 64, 1))
            pred_c = pc_c.predict(batch)
            pred_r = pc_r.predict(batch)
            for j in range(len(batch)):
                arrays[i*batch_size+j].column = pred_c[j][0]
                arrays[i*batch_size+j].rosette = pred_r[j][0]
        runtime.stop()

    def get_arrays(self, timespan=(0, 86400), area_ratio=(0, 1e9), x=(0, 1e9), y=(0, 1e9),
                   hit_ratio=(0, 1), aspect_ratio=(0, 1e9), alpha=(-360, 360),
                   c=(0, 1), r=(0, 1), timeshift=0):
        arrays = [array for array in self.arrays
                  if timespan[0] <= array.second+timeshift <= timespan[1]
                  and area_ratio[0] <= array.area_ratio() <= area_ratio[1]
                  and x[0] <= array.width() <= x[1]
                  and y[0] <= array.height() <= y[1]
                  and hit_ratio[0] <= array.hit_ratio <= hit_ratio[1]
                  and aspect_ratio[0] <= array.aspect_ratio <= aspect_ratio[1]
                  and alpha[0] <= array.alpha <= alpha[1]
                  and c[0] <= array.column <= c[1]
                  and r[0] <= array.rosette <= r[1]]
        return arrays

    def counts_per_second(self, timespan=(0, 86400), area_ratio=(0, 1e9), x=(0, 1e9), y=(0, 1e9),
                          hit_ratio=(0, 1), aspect_ratio=(0, 1e9), alpha=(-360, 360), c=(0, 1), r=(0, 1),
                          timeshift=0):
        arrays = self.get_arrays(timespan=timespan, area_ratio=area_ratio, x=x, y=y, hit_ratio=hit_ratio,
                                 aspect_ratio=aspect_ratio, alpha=alpha, c=c, r=r, timeshift=timeshift)
        counts = dict.fromkeys(range(self.arrays[0].second+timeshift,
                                     self.arrays[-1].second+timeshift + 1), 0)
        for a in arrays:
            counts[a.second+timeshift] += 1
        x, y = zip(*sorted(counts.items()))
        return np.array(x), np.array(y)

    # --- Plotting -----------------------------------------------------------------------------------------------------
    def __reset_plot(self):
        self.__n_figures = None
        self.__plt_iterator = None
        self.__fig = None
        self.__axes = None
        self.__auto_plot = None

    def __adjust_plot(self, i, title, xlabel, ylabel, grid, legend, log, index):

        if title is not None:
            self.__axes[i][0].title.set_text(title)
        if xlabel is not None:
            self.__axes[i][0].set_xlabel(xlabel)
        if ylabel is not None:
            self.__axes[i][0].set_ylabel(ylabel)
        if grid:
            self.__axes[i][0].grid()
        if legend:
            self.__axes[i][0].legend()
        if log:
            self.__axes[i][0].set_yscale("log")
        if index is None:
            self.__plt_iterator += 1
        if self.__auto_plot and self.__plt_iterator == self.__n_figures:
            self.show_plot()

    def init_plot(self, n_figures, tight_layout=True, auto_plot=False):
        self.__n_figures = n_figures
        self.__plt_iterator = 0
        # Squeeze must equal False for the variable self.__axes to be a 2d array for any number of subplots.
        self.__fig, self.__axes = plt.subplots(self.__n_figures, squeeze=False)
        self.__auto_plot = auto_plot
        if tight_layout:
            plt.tight_layout()

    def save_plot(self, filename):
        plt.savefig(filename)
        self.__reset_plot()

    def show_plot(self):
        plt.show()
        self.__reset_plot()

    def plot(self, timespan=(0, 86400), area_ratio=(0, 1e9), x=(0, 1e9), y=(0, 1e9),
             hit_ratio=(0, 1), aspect_ratio=(0, 1e9), alpha=(-360, 360), c=(0, 1), r=(0, 1),
             timeshift=0, index=None, color=None, fill_color=None, opacity=1.0, linewidth=1.0, fill=True,
             title=None, label=None, xlabel=None, ylabel=None, grid=False, legend=False, log=False):
        x, y = self.counts_per_second(timespan=timespan, area_ratio=area_ratio, x=x, y=y, hit_ratio=hit_ratio,
                                      aspect_ratio=aspect_ratio, alpha=alpha, c=c, r=r, timeshift=timeshift)
        if self.__plt_iterator is None:
            self.init_plot(1, tight_layout=False, auto_plot=True)
        i = self.__plt_iterator if index is None else index
        self.__axes[i][0].plot(x, y, color=color, alpha=opacity, label=label, linewidth=linewidth)
        if fill:
            self.__axes[i][0].fill_between(x, np.zeros(len(y)), y, alpha=opacity,
                                           color=color if fill_color is None else fill_color)
        self.__adjust_plot(i, title, xlabel, ylabel, grid, legend, log, index)

    def plot_count(self, timespan=(0, 86400), area_ratio=(0, 1e9), x=(0, 1e9), y=(0, 1e9),
                   hit_ratio=(0, 1), aspect_ratio=(0, 1e9), alpha=(-360, 360), c=(0, 1), r=(0, 1),
                   timeshift=0, index=None, color=None, opacity=1.0, title=None,
                   label=None, xlabel=None, ylabel=None, grid=False, legend=False, log=False):
        x, y = self.counts_per_second(timespan=timespan, area_ratio=area_ratio, x=x, y=y, hit_ratio=hit_ratio,
                                      aspect_ratio=aspect_ratio, alpha=alpha, c=c, r=r, timeshift=timeshift)
        if self.__plt_iterator is None:
            self.init_plot(1, tight_layout=False, auto_plot=True)
        i = self.__plt_iterator if index is None else index
        self.__axes[i][0].bar(x, y, align="center", width=1, color=color, alpha=opacity, label=label)
        self.__adjust_plot(i, title, xlabel, ylabel, grid, legend, log, index)

    # fix color bar !!!
    def plot_ratio(self, c0, c1, index=None, title=None, label=None, xlabel=None, ylabel=None,
                   grid=False, legend=False, log=False, opacity=1.0,
                   cmap="viridis", color_res=10, color_label=None, color_fixed=False):

        # ToDo: the time span must be the same for both counts!
        x0, y0 = self.counts_per_second(**c0)
        x1, y1 = self.counts_per_second(**c1)

        if self.__plt_iterator is None:
            self.init_plot(1, tight_layout=False, auto_plot=True)
        i = self.__plt_iterator if index is None else index

        colors = plt.cm.get_cmap(cmap, color_res)
        z = np.divide(y1, y0, out=np.zeros(y1.shape, dtype=float), where=y0 != 0)
        z_norm = np.interp(z, (z.min(), z.max()), (0, 1))
        self.__axes[i][0].bar(x0, y0, align="center", width=1, alpha=opacity, label=label,
                              color=colors(z) if color_fixed else colors(z_norm))

        # Create a mappable without a visual representation to
        # apply to the color bar. Typical matplotlib crap...
        s_map = plt.cm.ScalarMappable(cmap=colors, norm=plt.Normalize(z.min() if color_fixed else z.min(),
                                                                      z.max() if color_fixed else z.max()))
        # Using make_axes_locatable() to subdivide the axis. Otherwise it is not possible to
        # set the position of the color bar to the top.
        divider = make_axes_locatable(self.__axes[i][0])
        cax = divider.new_vertical(size="3%", pad=0)    # ToDo: make percentage adjustable!
        # Add divider to figure!
        self.__fig.add_axes(cax)
        colorbar = self.__fig.colorbar(s_map, cax=cax, orientation="horizontal")    # ticks=[0, 1]
        colorbar.set_label(color_label)
        colorbar.ax.xaxis.set_ticks_position("top")
        # Not needed at the moment, but I'll leave it in the code in case I need it.
        # Sadly, it's a pain in the ass to slog through the matplotlib doc.
        # colorbar.ax.set_xticklabels([z.min(), z.max()]) # xticks because of horizontal orientation
        # colorbar.ax.tick_params(labelsize=10)
        self.__adjust_plot(i, title, xlabel, ylabel, grid, legend, log, index)
