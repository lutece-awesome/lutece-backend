def get_username_strength( username ):
    """
        Return the report of username_strength as str.
        + username length should between 4 and 12 characters.
    """
    errormsg = ''
    try:
        if len( username ) < 4 or len( username ) > 12:
            errormsg = 'The length of username should bettween 6 and 12 characters.'
    except:
        errormsg = 'Unknown error.'
    finally:
        return errormsg


if __name__ == '__main__':
    print( get_username_strength( '12456' ) )
    print( get_username_strength( '1234563213213123123213131' ) )    
    print( get_username_strength( '123456' ) )
    print( get_username_strength( 'a123456' ) )
    print( get_username_strength( 'A123456' ) )
    print( get_username_strength( 'aaasdFeff' ) )
    print( get_username_strength( 'aA123456' ) )