from os import path, listdir
from .settings import META_FIELD, data_dir

def get_data( problem , data_type ):
    '''
        get data of data_type
    '''
    dr = path.join( data_dir , str( problem ) )
    li = list(filter( lambda x: path.splitext(x)[1] in META_FIELD[data_type] , listdir( dr ) ) )
    _send = {}
    for _ in li:
        f = open( path.join( dr , _ ) , "rb" )
        _send[_] = f.read()
        f.close()
    return _send


def cal_md5_or_create( problem , force = False ):
    '''
        Calcuate the md5-field of problem folder
        if force is True, always create/update md5 file
    '''
    try:
        dr = path.join( data_dir , str( problem ) )
        li = listdir( dr )
        if '.md5' in li and force is False:
            return True , None
        li = list( filter( lambda x : path.splitext( x )[1] in META_FIELD['md5-checker'] , li ) )
        args = []
        for _ in li:
            f = open( path.join( dr , _ ) , "rb" )
            md5 = hashlib.md5()
            md5.update( f.read() )
            content = md5.hexdigest()
            f.close()
            args.append( ( _ , content ) )
        args.sort()
        f = open( os.path.join( dr , '.md5' ) , "w" )
        f.write( str( args ) )
        f.close()
    except Exception as e:
        return False , str( e )
    return True , None


def process( request ):
    '''
        process the target request
    '''
    problem = request.POST.get( 'problem' )
    data_type = request.POST.get( 'data_type' )
    if data_type == 'md5-file':
        cal_md5_or_create( problem )
    return get_data( problem , data_type )