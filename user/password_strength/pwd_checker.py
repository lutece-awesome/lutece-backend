from re import compile, search

def get_password_strength( pwd ):
    """
        Return the report of password_strength as str list.
        + password length should between 6 and 12 characters.
        + password should contain at least one lowercase letter, one uppercase letter, one digit.
    """
    errormsg = []
    try:
        if len( pwd ) < 6 or len( pwd ) > 12:
            errormsg.append( 'The length of password should bettween 6 and 12 characters.' )
        if compile( '[a-z]' ).search( pwd ) == None:
            errormsg.append( 'Password should contain at least one lowercase letter.' )
        if compile( '[A-Z]' ).search( pwd ) == None:
            errormsg.append( 'Password should contain at least one uppercase letter.' )
        if compile( '\d' ).search( pwd ) == None:
            errormsg.append( 'Password should contain at least one digit.' )
    except:
        errormsg.clear()
        errormsg.append( 'Unknown error' )
    finally:
        return errormsg


if __name__ == '__main__':
    print( get_password_strength( '12456' ) )
    print( get_password_strength( '1234563213213123123213131' ) )    
    print( get_password_strength( '123456' ) )
    print( get_password_strength( 'a123456' ) )
    print( get_password_strength( 'A123456' ) )
    print( get_password_strength( 'aaasdFeff' ) )
    print( get_password_strength( 'aA123456' ) )