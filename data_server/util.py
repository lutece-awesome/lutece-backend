from os import path, listdir, mkdir, system
from .settings import META_FIELD, data_dir, ZIP_FIELD
import hashlib, random

def get_data( problem , data_type ):
    '''
        get data of data_type
    '''
    try:
        dr = path.join( data_dir , str( problem ) )
        li = list(filter( lambda x: path.splitext(x)[1] in META_FIELD[data_type] , listdir( dr ) ) )
        li.sort()
        _send = {}
        for _ in li:
            f = open( path.join( dr , _ ) , "rb" )
            _send[_] = f.read()
            f.close()
        return _send
    except:
        return None


def cal_md5_or_create( problem , force = False ):
    '''
        Calcuate the md5-field of problem folder
        if force is True, always create/update md5 file
    '''
    try:
        dr = path.join( data_dir , str( problem ) )
        li = listdir( dr )
        if 'data.md5' in li and force is False:
            return True , None
        li = list( filter( lambda x : path.splitext( x )[1] in META_FIELD['md5-check'] , li ) )
        args = []
        for _ in li:
            f = open( path.join( dr , _ ) , "rb" )
            md5 = hashlib.md5()
            md5.update( f.read() )
            content = md5.hexdigest()
            f.close()
            args.append( ( _ , content ) )
        args.sort()
        f = open( path.join( dr , 'data.md5' ) , "w" )
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
    data_type = request.POST.get( 'type' )
    if data_type == 'md5-file':
        cal_md5_or_create( problem )
    return get_data( problem , data_type )


def get_case_number( problem ):
    '''
        return case number
    '''
    dr = path.join( data_dir , str( problem ) )
    return len( list( filter( lambda x : path.splitext( x )[1] == '.in' , listdir( dr ) ) ) )

def check_upload_file( tempdir , errlist ):
    li = listdir( tempdir )
    fields = [ x for x in META_FIELD['test-data'] ] + [ x for x in ZIP_FIELD ]
    for each in li:
        if path.splitext( each )[1] not in fields:
            errlist.append( 'Unknown file ' + str( each ) )
            return False
    _in = list( filter( lambda x : path.splitext( x )[1] == '.in' , li ) )
    _out = list( filter( lambda x : path.splitext( x )[1] == '.out' , li ) )
    if len( _in ) != len( _out ):
        errlist.append( 'The number of input files ne the number of output files' )
        return False
    _in = [ path.splitext( x )[0] for x in _in ]
    _out = [ path.splitext( x )[0] for x in _out ]
    _in.sort()
    _out.sort()
    if _in != _out:
        errlist.append( 'Some input/output can not match' )
        return False
    return True

def upload_data( data , problem , errlist ):
    extension = path.splitext( data.name )[1]
    if extension not in ZIP_FIELD:
        errlist.append( 'Unsupported file extension, Lutece only support ' + str( [ x for x in ZIP_FIELD ] ) )
        return False
    random.seed()
    temp_dir = ''
    for i in range( 32 ):
        temp_dir = temp_dir + chr( random.randint( 0 , 25 ) + 65 )
    temp_dir = path.join( data_dir , temp_dir )
    mkdir( temp_dir )
    try:
        file = path.join( temp_dir , 'DATA-FILE' + extension )
        with open( file , 'wb' ) as destination:
            for chunk in data.chunks():
                destination.write( chunk )
        command = ZIP_FIELD[extension].format(
                path = temp_dir,
                sourcefile = file ) + ' 1>/dev/null 2>&1'
        system( command )
        check_upload_file( temp_dir , errlist )
        if len( errlist ) > 0:
            return False
        target = path.join( data_dir , str( problem ) )
        system( 'rm -rf ' + target )
        system( 'mv ' + temp_dir + ' ' + target )
        return True
    except Exception as e:
        print( str( e ) )
        errlist.append( str( e ) )
        return False
    finally:
        if path.exists( temp_dir ):
            system( 'rm -rf ' + temp_dir )