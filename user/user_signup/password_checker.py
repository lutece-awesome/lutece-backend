from re import compile, search


def get_password_strength(password):
    """
        Return the report of password_strength as str list.
        + password length should between 6 and 20 characters.
        + password should contain at least one lowercase letter, one uppercase letter, one digit.
    """
    errormsg = []
    try:
        if len(password) < 6 or len(password) > 20:
            errormsg.append(
                'The length of password should bettween 6 and 20 characters.')
        if compile('[a-z]').search(password) == None:
            errormsg.append(
                'Password should contain at least one lowercase letter.')
        if compile('[A-Z]').search(password) == None:
            errormsg.append(
                'Password should contain at least one uppercase letter.')
        if compile('\d').search(password) == None:
            errormsg.append('Password should contain at least one digit.')
    except:
        errormsg.clear()
        errormsg.append('Unknown error.')
    finally:
        return errormsg
