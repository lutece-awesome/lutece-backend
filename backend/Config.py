import configparser
import os

class ConfigReader:    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read( 'Lutece.conf' )

    @ property
    def perPagecount(self):
        return int( self.config.get( 'Page' , 'perPageCount' ) )

config = ConfigReader()

if __name__ == '__main__':
    print( config.perPagecount )
