import sys
import os.path
from FileHandler import FileHandler

class ErrorHandler(object):

    @staticmethod
    def verifyInputFile(settings):
        if not os.path.isfile(settings['i']):
            FileHandler.writeLineToFile(settings['e'], 'Error, cannot find valid input file.')
            sys.exit(2)


