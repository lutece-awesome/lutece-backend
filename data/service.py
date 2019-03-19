import zipfile
from os import path, mkdir, remove, listdir

from data.constant import DATA_PATH, INPUT_FILE_EXTENSION


class DataService:

    @staticmethod
    def get_cases_count(problem_pk):
        try:
            dr = path.join(path.expanduser(DATA_PATH), str(problem_pk))
            return len(list(filter(lambda x: path.splitext(x)[1] == INPUT_FILE_EXTENSION, listdir(dr))))
        except Exception:
            raise RuntimeError('Can not load test data folder.')

    @staticmethod
    def create_data_dir(problem_pk):
        try:
            dr = path.join(path.expanduser(DATA_PATH), str(problem_pk))
            mkdir(dr)
        except Exception:
            raise RuntimeError('Can not create data folder.')

    @staticmethod
    def clear_folder_and_extract_data(problem_pk, file):
        dr = path.join(path.expanduser(DATA_PATH), str(problem_pk))
        for each in listdir(dr):
            remove(path.join(dr, each))
        with zipfile.ZipFile(file) as zip_file:
            zip_file.extractall(path=dr)

    @staticmethod
    def check_datazip(file):
        zip_file = zipfile.ZipFile(file)
        file_list = zip_file.infolist()
        in_li = []
        out_li = []
        for each in file_list:
            name = each.filename.title()
            if name.find('.') < 0:
                raise RuntimeError('Unknown file name ' + name)
            spl = name.split('.')
            extension = spl[-1].lower()
            if extension != 'in' and extension != 'out':
                raise RuntimeError('Unknown file name ' + name)
            if extension == 'in':
                in_li.append(spl[:-1])
            elif extension == 'out':
                out_li.append(spl[:-1])
        if len(in_li) != len(out_li):
            raise RuntimeError('Input file number not equal output file number')
        for each in in_li:
            if each not in out_li:
                raise RuntimeError('Input / Output file not matching')
