from os import path, listdir, mkdir, system
from data.constant import META_FIELD, DATA_PATH
import hashlib, random

def get_data( problem , data_type ):
    '''
        get data of data_type
    '''
    try:
        dr = path.join( path.expanduser( DATA_PATH ) , str( problem ) )
        li = list(filter( lambda x: path.splitext(x)[1] in META_FIELD.get( data_type ) , listdir( dr ) ) )
        li.sort()
        _send = {}
        for _ in li:
            with open( path.join( dr , _ ) , "rb" ) as file:
                _send[_] = file.read()                
        return _send
    except:
        return None


def cal_md5_or_create( problem , force = False ):
    '''
        Calcuate the md5-field of problem folder
        if force is True, always create/update md5 file
    '''
    try:
        dr = path.join( path.expanduser( DATA_PATH ) , str( problem ) )
        li = listdir( dr )
        if 'data.md5' in li and force is False:
            return True , None
        li = list( filter( lambda x : path.splitext( x )[1] in META_FIELD['md5-check'] , li ) )
        args = []
        for _ in li:
            with open( path.join( dr , _ ) , "rb" ) as file:
                md5 = hashlib.md5()
                md5.update( file.read() )
            content = md5.hexdigest()
            args.append( ( _ , content ) )
        args.sort()
        with open( path.join( dr , 'data.md5' ) , "w" ) as file:
            file.write( str( args ) )
    except Exception as e:
        return False , str( e )
    return True , None


def process( request ):
    '''
        process the target request
    '''
    problem = request.POST.get( 'problem' )
    data_type = request.POST.get( 'type' )
    if data_type == 'md5-file':
        cal_md5_or_create( problem )
    return get_data( problem , data_type )