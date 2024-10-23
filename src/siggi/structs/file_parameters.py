from enum import IntEnum

import attr

DEFAULT_FFT_SIZE = 1024

class DataType(IntEnum):
    COMPLEX = 0
    REAL = 1

@attr.s
class FileParameters:
    samplerate_hz = attr.ib(type=float)
    sample_period = attr.ib(type=float)
    path = attr.ib(type=str)
    n_samples = attr.ib(type=int)
    fft_size = attr.ib(type=int, default=DEFAULT_FFT_SIZE)
    data_type = attr.ib(type=DataType, default=DataType.REAL)
    shrinked_size_to_real_size_ratio = attr.ib(type=float, default=1.0)

    @classmethod
    def create(cls, fs, path, n_samples, fft_size=DEFAULT_FFT_SIZE):
        sample_period = 1/fs
        return cls(fs, sample_period, path, n_samples, fft_size)
