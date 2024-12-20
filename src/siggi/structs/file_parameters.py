import logging
from enum import IntEnum

import attr
import numpy as np

MAX_FFT_SIZE = 65536

class DataType(IntEnum):
    COMPLEX = 0
    REAL = 1

@attr.s
class FileParameters:
    samplerate_hz = attr.ib(type=float)
    sample_period = attr.ib(type=float)
    path = attr.ib(type=str)
    n_samples = attr.ib(type=int)
    fft_size = attr.ib(type=int, default=MAX_FFT_SIZE)
    data_type = attr.ib(type=DataType, default=DataType.REAL)
    shrinked_size_to_real_size_ratio = attr.ib(type=float, default=1.0)
    fft_ref = attr.ib(type=float, default=1.0)

    def update_samplerate(self, fs):
        self.sample_period = 1/fs
        self.samplerate_hz = fs

    @staticmethod
    def choose_fft_size(fs_in, n_samples):
        window = fs_in // 10
        fft_size = min(MAX_FFT_SIZE, 2**(int(round(np.log2(window))) + 1))
        fft_size = min(fft_size, n_samples)
        logging.info(f'Setting fft size to {fft_size}.')
        return fft_size

    @classmethod
    def create(cls, fs, path, n_samples, fft_size=MAX_FFT_SIZE, data_type=DataType.REAL):
        sample_period = 1/fs
        return cls(fs, sample_period, path, n_samples, fft_size, data_type)
