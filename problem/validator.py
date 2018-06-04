from re import compile

def check_title( title , err ):
    if len( title ) == 0:
        err.append( 'Title can not be empty' )
        return False
    elif len( title ) > 32:
        err.append( 'Title\'s length can not longer than 32' )
        return False
    return True


def check_timelimit( timelimit , err ):
    if compile('\D').search(timelimit) != None:
        err.append( 'Type of timelimit should be number' )
        return
    timelimit = int( timelimit )
    if timelimit < 0:
        err.append( 'Timelimit should be non-negative' )
    elif timelimit > 20000:
        err.append( 'Timelimit should no more than 20 seconds' )


def check_memorylimit( memorylimit , err ):
    if compile('\D').search(memorylimit) != None:
        err.append( 'Type of memorylimit should be number' )
        return
    memorylimit = int( memorylimit )
    if memorylimit < 0:
        err.append( 'Memorylimit should be non-negative' )
    elif memorylimit > 1024:
        err.append( 'Memorylimit should no more than 1 GB' )