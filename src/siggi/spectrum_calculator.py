import numpy as np
from scipy.fft import fft, fftfreq

FFT_SIZE = 1024

fs = 10e3
T = 1/fs

class SpectrumCalculator():
    def __init__(self, raw_samples, spectrum_updater):
        self.spectrum_updater = spectrum_updater
        self.raw_samples = raw_samples
        self.calc_initial_sample_selection()
        self.calc_frequency_axes()
        self.xf, self.yf = np.array([]), np.array([])

    def calc_initial_sample_selection(self):
        self.selected_samples = self.raw_samples[:FFT_SIZE]

    def calc_frequency_axes(self):
        self.xf = fftfreq(FFT_SIZE, T)[:FFT_SIZE // 2]

    def calc_new_samples_selection(self, new_center):
        if new_center < FFT_SIZE//2:
            new_center = FFT_SIZE//2

        if new_center > self.raw_samples.size- FFT_SIZE//2:
            new_center = self.raw_samples.size- FFT_SIZE//2

        self.selected_samples = self.raw_samples[new_center - FFT_SIZE//2:new_center + FFT_SIZE//2]

    def notifyUpdate(self, new_center):
        self.calc_new_samples_selection(new_center)
        self.calc_new_spectrum()
        self.spectrum_updater.update_spectrum((self.xf, self.yf))

    def calc_new_spectrum(self):
        self.yf = 2.0/FFT_SIZE * np.abs(fft(self.selected_samples)[:FFT_SIZE // 2])
