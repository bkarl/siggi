import numpy as np
from scipy.fft import fft, fftfreq

class SpectrumCalculator():
    def __init__(self, raw_samples, spectrum_updater, file_params):
        self.spectrum_updater = spectrum_updater
        self.raw_samples = raw_samples
        self.file_params = file_params
        self.xf, self.yf = np.array([]), np.array([])
        self.calc_initial_sample_selection()
        self.calc_frequency_axes()

    def calc_initial_sample_selection(self):
        self.selected_samples = self.raw_samples[:self.file_params.fft_size]

    def calc_frequency_axes(self):
        self.xf = fftfreq(self.file_params.fft_size, self.file_params.sample_period)[:self.file_params.fft_size // 2]

    def calc_new_samples_selection(self, new_center):
        if new_center < self.file_params.fft_size//2:
            new_center = self.file_params.fft_size//2

        if new_center > self.raw_samples.size- self.file_params.fft_size//2:
            new_center = self.raw_samples.size- self.file_params.fft_size//2

        self.selected_samples = self.raw_samples[new_center - self.file_params.fft_size//2:new_center + self.file_params.fft_size//2]

    def notifyUpdate(self, new_center):
        self.calc_new_samples_selection(new_center)
        self.calc_new_spectrum()
        self.spectrum_updater.update_spectrum((self.xf, self.yf))

    def calc_new_spectrum(self):
        self.yf = 2.0/self.file_params.fft_size * np.abs(fft(self.selected_samples)[:self.file_params.fft_size // 2])
