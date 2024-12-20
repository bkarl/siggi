import argparse
import logging
import os
import threading

import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.cbook import file_requires_unicode
from matplotlib.patches import Rectangle
from matplotlib.ticker import EngFormatter
from numpy.fft import fftshift

from blit_manager import BlitManager
from scipy.fft import fft, fftfreq
from scipy import signal
from sample_selector import SampleSelector
from siggi.file_handling.file_reader import FileReader
from siggi.file_handling.file_reader_factory import FileReaderFactory
from siggi.file_handling.file_reader_progress_bar import FileReaderProgressBar
from siggi.file_handling.file_selector import DataImportForm
from siggi.structs.file_parameters import FileParameters, DataType
from spectrum_calculator import SpectrumCalculator
from spectrum_updater import SpectrumUpdater
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import attr

NUM_POINTS = 16384
FS = 10e3
logging.getLogger().setLevel(logging.INFO)

@attr.s
class Siggi:
    params = attr.ib(type=FileParameters)
    file_reader = attr.ib(type=FileReader)

    @classmethod
    def create(cls, file_params, file_reader):
        return cls(file_params, file_reader)

    def create_windows_and_render(self):
        fig_spec, spec_line = self.create_spectrum_window()
        fig_samples, rect = self.create_waterfall_window()
        fig_spec.canvas.manager.set_window_title(os.path.basename(self.params.path))
        fig_samples.canvas.manager.set_window_title(os.path.basename(self.params.path))
        su = SpectrumUpdater(fig_spec.canvas, spec_line)
        sc = SpectrumCalculator.create(self.params, su, self.file_reader)
        sss = SampleSelector(fig_samples.canvas, sample_selector=rect, spectrum_calculator=sc, file_params=self.params)
        plt.show()

    def create_waterfall_window(self):
        fig_samples, ax_samples = plt.subplots()
        ax_samples.specgram(self.file_reader.file_contents, NFFT=self.params.fft_size, Fs=self.params.samplerate_hz)
        formatter = EngFormatter(unit="Hz", places=1)
        ax_samples.yaxis.set_major_formatter(formatter)
        y0, y1 = ax_samples.get_ybound()
        ysize = abs(y0) + abs(y1)
        # Get the current x-tick values
        current_ticks = ax_samples.get_xticks()
        ax_samples.set(xlabel="time/s", ylabel="Frequency")
        ax_samples.set_title('Spectogram')
        # Double the tick values
        new_ticks = current_ticks * self.params.shrinked_size_to_real_size_ratio

        # Set the new tick values on the x-axis
        ax_samples.set_xticklabels([f"{tick:.2f}" for tick in new_ticks])  # Update the tick labels

        # add a line
        fftwidth_sec = self.params.fft_size / self.params.samplerate_hz
        rect = Rectangle((0, y0), fftwidth_sec, ysize, animated=True, linestyle='-', alpha=0.3, linewidth=1)
        ax_samples.add_patch(rect)
        return fig_samples, rect

    def create_spectrum_window(self):
        fig_spec, ax_spec = plt.subplots()
        yf = fft(self.file_reader.file_contents[:self.params.fft_size] * np.hanning(self.params.fft_size))
        xf = fftfreq(self.params.fft_size, self.params.sample_period)
        if self.params.data_type == DataType.COMPLEX:
            xf = fftshift(xf)
            yf = fftshift(yf)
        else:
            xf = xf[:self.params.fft_size // 2]
            yf = yf[:self.params.fft_size // 2]
        yf = 2.0 / self.params.fft_size * np.abs(yf)
        spec_line, = ax_spec.plot(xf, 20 * np.log10(yf/self.params.fft_ref), animated=True)
        formatter = EngFormatter(unit="Hz", places=1)
        ax_spec.xaxis.set_major_formatter(formatter)
        ax_spec.set(xlabel="Frequency", ylabel="Power/dbFS")
        ax_spec.set_title('Spectrum')
        ax_spec.grid(True, which='major', axis='both', linestyle=':')
        #ax_spec.set_ylim(0, 1e6)
        return fig_spec, spec_line


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='siggi',
        description='spectrum analyzer')

    parser.add_argument('filename', nargs='?', default='')  # positional optional argument
    args = parser.parse_args()

    app = DataImportForm()
    app.run()
    param = app.get_file_parameters()
    file_reader = FileReaderFactory.get_correct_file_reader(param)
    if file_reader.is_large_file():
        pb = FileReaderProgressBar()
        file_reader.set_progress_bar(pb)
        thread = threading.Thread(target=file_reader.loadFile)
        thread.start()
        pb.render()
    else:
        file_reader.loadFile()
    siggi = Siggi.create(param, file_reader)
    siggi.create_windows_and_render()

