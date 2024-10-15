import attr
import numpy as np

from siggi.structs.file_parameters import FileParameters, DataType


@attr.s
class FileReader():
    file_params = attr.ib(type=FileParameters)
    file_contents = attr.ib(type=np.ndarray, default=np.zeros(0))

    def loadFile(self):
        self.file_contents = np.load(self.file_params.path)
        self.file_params.n_samples = self.file_contents.size

        if 'complex' in self.file_contents.dtype.name:
            self.file_params.data_type = DataType.COMPLEX
