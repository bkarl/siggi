import attr

DEFAULT_FFT_SIZE = 1024

@attr.s
class FileParameters:
    samplerate_hz = attr.ib(type=float)
    sample_period = attr.ib(type=float)
    path = attr.ib(type=str)
    n_samples = attr.ib(type=int)
    fft_size = attr.ib(type=int, default=DEFAULT_FFT_SIZE)

    @classmethod
    def create(cls, fs, path, n_samples, fft_size=DEFAULT_FFT_SIZE):
        sample_period = 1/fs
        return cls(fs, sample_period, path, n_samples, fft_size)
