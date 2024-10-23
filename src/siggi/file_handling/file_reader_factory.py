from siggi.file_handling.file_reader_npy import FileReaderNpy
from siggi.structs.file_parameters import FileParameters

class FileReaderFactory:
    @staticmethod
    def get_correct_fileread(param: FileParameters):
        if '.npy' in param.path:
            file_reader = FileReaderNpy(param)
        return file_reader