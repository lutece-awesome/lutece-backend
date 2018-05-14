a = dict()
a[1]=2
a['dsa']=3
print(a)

b = False

if not b:
	print( "not" )
else:
	print( 'yes' )

from random import randint

a , b = map( int , input().split())

if randint( 1 , 5 ) == 1:
    print( a + b )
else:
    print( a + b + 2 )
