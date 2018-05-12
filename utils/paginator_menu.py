from Lutece.config import PER_PAGINATOR_COUNT


def get_range( page , maxpage ):
    before = PER_PAGINATOR_COUNT >> 1
    after = PER_PAGINATOR_COUNT - 1 - before
    l = max( 1 , page - before )
    r = min( maxpage , page + after )
    rl = before - ( page - l )
    rr = after - ( r - page )
    l = max( 1 , l - rr )
    r = min( maxpage , r + rl )
    return range( l , r + 1 )