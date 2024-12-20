import logging
from abc import abstractmethod
from multiprocessing.pool import ThreadPool

import attr
import numpy as np
import os

from siggi.structs.file_parameters import FileParameters, DataType

MAX_FILE_SIZE = 100e6
MAX_MEMORY_SIZE_MB = 512

@attr.s
class FileReader:
    file_params = attr.ib(type=FileParameters)
    file_contents = attr.ib(type=np.ndarray, default=np.zeros(0))

    def is_large_file(self):
        return os.path.getsize(self.file_params.path) > MAX_FILE_SIZE

    def loadFile(self):
        if self.is_large_file():
            self.load_large_file()
        else:
            self.load_small_file()
        self.file_params.n_samples = self.file_contents.size
        self.check_datatype()
        self._choose_fft_size()

    def _choose_fft_size(self):
        self.file_params.fft_size = FileParameters.choose_fft_size(self.file_params.samplerate_hz, self.file_contents.size)

    def check_datatype(self):
        if 'complex' in self.file_contents.dtype.name:
            self.file_params.data_type = DataType.COMPLEX

    @abstractmethod
    def load_small_file(self):
        raise NotImplementedError()

    def set_progress_bar(self, pb):
        self.pb = pb

    def load_large_file(self):
        max_size_bytes = MAX_MEMORY_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        # Get the array shape and data type from the file header
        n_elements, element_size_byte, self.dtype = self.get_file_meta()

        block_size = self.file_params.fft_size
        # Calculate the maximum number of elements that can fit in the resulting array
        max_elements = max_size_bytes // element_size_byte

        # Calculate the number of blocks we can fit into the result array
        num_blocks = int(min(n_elements // block_size, max_elements // block_size))

        # Determine the indices to sample blocks from the original array
        block_indices = np.linspace(0, n_elements - block_size, num_blocks, dtype=int)

        # Create the resulting array to store the sampled data
        resulting_shape = (num_blocks, block_size)
        self.file_contents = np.empty(resulting_shape, dtype=self.dtype)

        self.mapped_file = self.map_large_file()
        self.pb.set_max(block_indices.size)
        # Read blocks of block_size elements and store in the result array
        with ThreadPool(processes=8) as pool:
            pool.starmap(self.copy_to_shrinked_array, enumerate(block_indices))

        self.file_contents = self.file_contents.flatten()
        self.file_params.shrinked_size_to_real_size_ratio = n_elements / max_elements
        self.convert_file_contents()
        self.pb.close()

    def copy_to_shrinked_array(self, i, idx):
        actual_idx = idx
        if self.dtype == np.int16:
            actual_idx = idx * 2
        self.file_contents[i] = self.mapped_file[actual_idx:actual_idx + self.file_params.fft_size]
        self.pb.update()

    def convert_file_contents(self):
        pass

    @abstractmethod
    def map_large_file(self):
        raise NotImplementedError()

    @abstractmethod
    def get_file_meta(self):
        raise NotImplementedError()