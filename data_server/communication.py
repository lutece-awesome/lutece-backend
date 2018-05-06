from pickle import loads
from . settings import header_length, buffersize

def read_header_length( msg ):
    package_length = 0
    for _ in range( header_length ):
        package_length = ( package_length << 1 ) + int( msg[_] ) - ord( '0' )
    return package_length + header_length

def recv_data( soc ):
    msg = []
    curlen = 0
    maxlength = -1
    while True:
        data = soc.recv( buffersize )
        msg.append( data )
        curlen += len( data )
        if curlen >= header_length and maxlength == -1:
            maxlength = read_header_length( ( b''.join( msg ) ) )
        if curlen == maxlength:
            break
    msg = b''.join( msg )
    return loads( msg[header_length:] )

def send_data( soc , data ):
    length = len( data )
    header_str = ''
    for _ in range( header_length ):
        header_str += str( length & 1 )
        length >>= 1
    header_str = header_str[::-1]
    soc.sendall( header_str.encode( 'ascii' ) + data )