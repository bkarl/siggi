import argparse

import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.cbook import file_requires_unicode
from matplotlib.patches import Rectangle
from numpy.fft.helper import fftshift

from blit_manager import BlitManager
from scipy.fft import fft, fftfreq
from scipy import signal
from sample_selector import SampleSelector
from siggi.file_handling.file_reader import FileReader
from siggi.file_handling.file_selector import DataImportForm
from siggi.structs.file_parameters import FileParameters, DataType
from spectrum_calculator import SpectrumCalculator
from spectrum_updater import SpectrumUpdater
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import attr

NUM_POINTS = 16384
FFT_SIZE = 1024
FS = 10e3

@attr.s
class Siggi:
    params = attr.ib(type=FileParameters)
    file_reader = attr.ib(type=FileReader)

    @classmethod
    def create(cls, file_params):
        file_reader = FileReader(file_params)
        file_reader.loadFile()
        return cls(file_params, file_reader)

    def create_windows_and_render(self):
        fig_spec, spec_line = self.create_spectrum_window()
        fig_samples, rect = self.create_waterfall_window()
        su = SpectrumUpdater(fig_spec.canvas, spec_line)
        sc = SpectrumCalculator.create(self.params, su, self.file_reader)
        sss = SampleSelector(fig_samples.canvas, sample_selector=rect, spectrum_calculator=sc, file_params=self.params)
        plt.show()

    def create_waterfall_window(self):
        fig_samples, ax_samples = plt.subplots()
        ax_samples.specgram(self.file_reader.file_contents, NFFT=self.params.fft_size, Fs=self.params.samplerate_hz)
        y_size = ax_samples.get_ylim()
        # add a line
        fftwidth_sec = self.params.fft_size / self.params.samplerate_hz
        rect = Rectangle((0, y_size[0]), fftwidth_sec, y_size[1], animated=True, linestyle='-', alpha=0.3, linewidth=1)
        ax_samples.add_patch(rect)
        return fig_samples, rect

    def create_spectrum_window(self):
        fig_spec, ax_spec = plt.subplots()
        yf = fft(self.file_reader.file_contents[:self.params.fft_size])
        xf = fftfreq(self.params.fft_size, self.params.sample_period)
        if self.params.data_type == DataType.COMPLEX:
            xf = fftshift(xf)
            yf = fftshift(yf)
        else:
            xf = xf[:self.params.fft_size // 2]
            yf = yf[:self.params.fft_size // 2]
        spec_line, = ax_spec.plot(xf, 2.0 / self.params.fft_size * np.abs(yf), animated=True)
        #ax_spec.set_ylim(0, 1e6)
        return fig_spec, spec_line


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='siggi',
        description='spectrum analyzer')

    parser.add_argument('filename', nargs='?', default='')  # positional optional argument
    args = parser.parse_args()

    #if not
    app = DataImportForm()
    app.run()
    param = app.get_file_parameters()
    siggi = Siggi.create(param)
    siggi.create_windows_and_render()

