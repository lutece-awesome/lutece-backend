from django.test import TestCase
from data.service import DataService

class TestSerivce( TestCase ):

    def testABC( self ):
        DataService.extract_data( 1 )
