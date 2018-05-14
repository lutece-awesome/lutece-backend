# Lutece data dir
from os import path

data_dir = path.join( path.dirname(path.abspath(__file__)) , 'Lutece_Data' )

# field
META_FIELD = {
    'test-data' : ['.in' , '.out'],
    'md5-check' : ['.in' , '.out'],
    'md5-file' : ['.md5']
}

ZIP_FIELD = {
    '.zip' : 'unzip -d {path} {sourcefile}',
    '.tar' : 'tar -xvf {sourcefile} -C {path}',
}