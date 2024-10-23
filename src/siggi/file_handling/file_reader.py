from abc import abstractmethod

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

    def loadFile(self):
        if os.path.getsize(self.file_params.path) > MAX_FILE_SIZE:
            self.load_large_file()
        else:
            self.load_small_file()
        self.file_params.n_samples = self.file_contents.size
        self.check_datatype()

    def check_datatype(self):
        if 'complex' in self.file_contents.dtype.name:
            self.file_params.data_type = DataType.COMPLEX

    @abstractmethod
    def load_small_file(self):
        raise NotImplementedError()

    def load_large_file(self):
        max_size_bytes = MAX_MEMORY_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        block_size = self.file_params.fft_size
        # Get the array shape and data type from the .npy file header
        n_elements, element_size_byte, dtype = self.get_file_meta()

        # Calculate the maximum number of elements that can fit in the resulting array
        max_elements = max_size_bytes // element_size_byte

        # Calculate the number of blocks we can fit into the result array
        num_blocks = int(min(n_elements // block_size, max_elements // block_size))

        # Determine the indices to sample blocks from the original array
        block_indices = np.linspace(0, n_elements - block_size, num_blocks, dtype=int)

        # Create the resulting array to store the sampled data
        resulting_shape = (num_blocks, block_size)
        self.file_contents = np.empty(resulting_shape, dtype=dtype)

        data = self.map_large_file()
        # Read blocks of 1024 elements and store in the result array
        for i, idx in enumerate(block_indices):
            self.file_contents[i] = data[idx:idx + block_size]
        self.file_contents = self.file_contents.flatten()
        self.file_params.shrinked_size_to_real_size_ratio = n_elements / max_elements

    @abstractmethod
    def map_large_file(self):
        raise NotImplementedError()

    @abstractmethod
    def get_file_meta(self):
        raise NotImplementedError()