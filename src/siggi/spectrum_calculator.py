import attr
import numpy as np
from numpy.fft.helper import fftshift
from scipy.fft import fft, fftfreq

from siggi.file_handling.file_reader import FileReader
from siggi.spectrum_updater import SpectrumUpdater
from siggi.structs.file_parameters import FileParameters, DataType


@attr.s
class SpectrumCalculator:
    file_params = attr.ib(type=FileParameters)
    spectrum_updater = attr.ib(type=SpectrumUpdater)
    file_reader = attr.ib(type=FileReader)
    xf = attr.ib(default=np.array([]))
    yf = attr.ib(default=np.array([]))

    @classmethod
    def create(cls, file_params, spectrum_updater, file_reader):
        xf = SpectrumCalculator.calc_frequency_axes(file_params)
        return cls(file_params, spectrum_updater, file_reader, xf)

    @staticmethod
    def calc_frequency_axes(params: FileParameters):
        if params.data_type == DataType.COMPLEX:
            return fftshift(fftfreq(params.fft_size, params.sample_period))
        return fftfreq(params.fft_size, params.sample_period)[:params.fft_size // 2]

    def calc_new_samples_selection(self, new_center):
        if new_center < self.file_params.fft_size//2:
            new_center = self.file_params.fft_size//2

        if new_center > self.file_params.n_samples - self.file_params.fft_size//2:
            new_center = self.file_params.n_samples - self.file_params.fft_size//2

        self.selected_samples = self.file_reader.file_contents[new_center - self.file_params.fft_size//2:new_center + self.file_params.fft_size//2]

    def notifyUpdate(self, new_center):
        self.calc_new_samples_selection(new_center)
        self.calc_new_spectrum()
        self.spectrum_updater.update_spectrum((self.xf, self.yf))

    def calc_new_spectrum(self):
        self.yf = 2.0 / self.file_params.fft_size * np.abs(fft(self.selected_samples * np.hanning(self.file_params.fft_size)))
        self.yf = 20 * np.log10(self.yf/self.file_params.fft_ref)
        if self.file_params.data_type == DataType.COMPLEX:
            self.yf = fftshift(self.yf)
        else:
            self.yf = self.yf[:self.file_params.fft_size // 2]
