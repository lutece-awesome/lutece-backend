from re import compile,findall
from validate_email import validate_email


def get_email_report( email ):
    """
        Return the report of email as str.
        + check whether the given email is valid or not.
    """
    errormsg = ''
    try:
        if validate_email( email ) == False:
            errormsg = 'Invailed email address.'
    except:
        errormsg = 'Unknown error.'
    finally:
        return errormsg


if __name__ == '__main__':
    print( get_email_report( 'xipersup@mgail.com' ) )
    print( get_email_report( 'xianyu1121mgail.com' ) )