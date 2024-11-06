import pathlib
import re

import attr
import numpy as np
import os

from siggi.file_handling.file_reader import FileReader
from siggi.structs.file_parameters import FileParameters, DataType

@attr.s
class FileReaderWvd(FileReader):
    def __attrs_post_init__(self):
        self.file_params.fft_ref = 2**15
    def load_small_file(self):
        self.file_contents = np.fromfile(self.file_params.path, dtype=np.int16)
        self.convert_file_contents()

    def get_file_meta(self):
        clock_pattern = r"CLOCK:(\d+\.\d+)"
        samples_pattern = r"SAMPLES:(\d+)"

        meta_path = self.replace_file_suffix(self.file_params.path, '.wvh')

        with open(meta_path, 'r') as f:
            text = f.read()
            clock_match = re.search(clock_pattern, text)
            samples_match = re.search(samples_pattern, text)

        if clock_match and samples_match:
            clock_value = float(clock_match.group(1))
            n_elements = int(samples_match.group(1))
        else:
            raise RuntimeError("Could not extract file metadata.")

        dtype = np.int16
        element_size_byte = np.dtype(dtype).itemsize

        self.file_params.update_samplerate(clock_value)

        return n_elements, element_size_byte, dtype

    def convert_file_contents(self):
        self.file_contents = self.file_contents[::2] + 1j * self.file_contents[1::2]

    def replace_file_suffix(self, path, new_suffix):
        path = pathlib.Path(path)
        return str(path.parent / (path.stem + new_suffix))

    def map_large_file(self):
        # Use np.memmap to memory-map the original file
        return np.memmap(self.file_params.path, mode='r', dtype=np.int16)
