import socket , pickle , logging , os , hashlib 
from . settings import data_dir, META_FIELD, port, max_connection
from . communication import recv_data, send_data

def cal_md5_or_create( problem , force = False ):
    '''
        Calcuate the md5-field of problem folder
        if force is True, always create/update md5 file
    '''
    try:
        path = os.path.join( data_dir , str( problem ) )
        li = os.listdir( path )
        if 'md5' in li and force is False:
            return True
        li = list( filter( lambda x : os.path.splitext( x )[1] in META_FIELD['md5'] , li ) )
        kwargs = []
        for _ in li:
            f = open( os.path.join( path , _ ) , "rb" )
            md5 = hashlib.md5()
            md5.update( f.read() )
            content = md5.hexdigest()
            f.close()
            kwargs.append( ( _ , content ) )
        kwargs.sort()
        f = open( os.path.join( path , 'md5' ) , "w" )
        f.write( str( kwargs ) )
        f.close()
    except Exception as e:
        return False , str( e )
    return True

def process( soc , problem , data_type ):
    try:
        path = os.path.join( data_dir , str( problem ) )
        if data_type == 'md5':
            cal_md5_or_create( problem )
            f = open( os.path.join( path , 'md5' ) , "rb" )
            send_data( soc , pickle.dumps( f.read() , 2 ) )
            f.close()
            return True
        li = list(filter( lambda x: os.path.splitext(x)[1] in META_FIELD[data_type] , os.listdir( path ) ))
        li.sort()
        rcv = {}
        for _ in li:
            f = open( os.path.join( path , _ ) , "rb" )
            rcv[_] = f.read()
            f.close()
        send_data( soc , pickle.dumps( rcv , 2 ) )
    except:
        return False
    return True

def run_data_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    s.bind( ( ip , port ) )  
    s.listen( max_connection )
    print( 'Dataserver start completed, new listen ' + str(ip) + ':' + str(port) )
    while True:
        soc , add = s.accept()
        print( 'Listen ' + str( add ) )
        try:
            js = recv_data( soc )
            process( soc , js['problem'] , js['type']  )
        finally:
            print( 'Close ' + str( add ) )
            soc.close()