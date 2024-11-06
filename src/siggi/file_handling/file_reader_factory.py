from siggi.file_handling.file_reader_npy import FileReaderNpy
from siggi.file_handling.file_reader_wvd import FileReaderWvd
from siggi.structs.file_parameters import FileParameters

class FileReaderFactory:
    @staticmethod
    def get_correct_file_reader(param: FileParameters):
        if '.npy' in param.path:
            file_reader = FileReaderNpy(param)

        if '.wvd' in param.path:
            file_reader = FileReaderWvd(param)
        return file_reader