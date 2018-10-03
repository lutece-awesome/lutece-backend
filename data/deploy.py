from os.path import join, abspath, dirname
from os import system

USER_NAME = 'lutece_data_user'
DATA_DIR = 'trunk'
PATH = abspath( dirname( __file__ ) )
DATA_PATH = join( PATH , DATA_DIR )

def create_data_dir( path ):
    script = f'mkdir {path}'
    print( f'- Creating data server at {path}, script is `{script}`.' )
    system( script )
    print( f'- Done' )

def create_user():

    pass

print( DATA_PATH )
