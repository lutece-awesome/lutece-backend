def get_username_strength(username):
    """
        Return the report of username_strength as str.
        + username length should between 4 and 12 characters.
    """
    errormsg = ''
    try:
        if len(username) < 4 or len(username) > 12:
            errormsg = 'The length of username should bettween 4 and 12 characters.'
    except:
        errormsg = 'Unknown error.'
    finally:
        return errormsg
