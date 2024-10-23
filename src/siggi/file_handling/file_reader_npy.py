import attr
import numpy as np
import os

from siggi.file_handling.file_reader import FileReader
from siggi.structs.file_parameters import FileParameters, DataType

MAX_FILE_SIZE = 100e6
MAX_MEMORY_SIZE_MB = 512

@attr.s
class FileReaderNpy(FileReader):

    def load_small_file(self):
        self.file_contents = np.load(self.file_params.path)

    def get_file_meta(self):
        with open(self.file_params.path, 'rb') as f:
            version = np.lib.format.read_magic(f)
            shape, _, dtype = np.lib.format.read_array_header_1_0(f)

        n_elements = shape[0]
        element_size_byte = np.dtype(dtype).itemsize

        return n_elements, element_size_byte, dtype

    def map_large_file(self):
        # Use np.memmap to memory-map the original file
        return np.lib.format.open_memmap(self.file_params.path, mode='r')