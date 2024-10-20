import attr
import numpy as np
import os

from siggi.structs.file_parameters import FileParameters, DataType

MAX_FILE_SIZE = 100e6

@attr.s
class FileReader():
    file_params = attr.ib(type=FileParameters)
    file_contents = attr.ib(type=np.ndarray, default=np.zeros(0))

    def loadFile(self):
        if os.path.getsize(self.file_params.path) > MAX_FILE_SIZE:
            self.shrink_array()
        else:
            self.file_contents = np.load(self.file_params.path)
        self.file_params.n_samples = self.file_contents.size

        if 'complex' in self.file_contents.dtype.name:
            self.file_params.data_type = DataType.COMPLEX


    def shrink_array(self, max_size_mb=512):
        max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
        block_size = self.file_params.fft_size
        # Get the array shape and data type from the .npy file header
        with open(self.file_params.path, 'rb') as f:
            version = np.lib.format.read_magic(f)
            shape, _, dtype = np.lib.format.read_array_header_1_0(f)

        # Calculate the maximum number of elements that can fit in the resulting array
        max_elements = max_size_bytes // np.dtype(dtype).itemsize

        # Calculate the number of blocks we can fit into the result array
        num_blocks = int(min(shape[0] // block_size, max_elements // (block_size * np.prod(shape[1:]))))

        # Determine the indices to sample blocks from the original array
        block_indices = np.linspace(0, shape[0] - block_size, num_blocks, dtype=int)

        # Create the resulting array to store the sampled data
        resulting_shape = (num_blocks, block_size) + shape[1:]
        self.file_contents = np.empty(resulting_shape, dtype=dtype)

        # Use np.memmap to memory-map the original file
        data = np.lib.format.open_memmap(self.file_params.path, dtype=dtype, mode='r', shape=shape)

        # Read blocks of 1024 elements and store in the result array
        for i, idx in enumerate(block_indices):
            self.file_contents[i] = data[idx:idx + block_size]
        self.file_contents = self.file_contents.flatten()
