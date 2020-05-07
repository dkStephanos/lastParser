import sys
import argparse

class CLIInterface(object):
    
    #Constructor takes in std options
    def __init__(self, stdin, stdout, stderr, lang):
        self.input_file = stdin
        self.markup_file = stdout
        self.error_file = stderr
        self.suspense_file = stderr
        self.markup_lang = lang


    #Logs status and code to screen
    @staticmethod
    def log(status, code):
        print(status + "Exiting with code 2\n" if code == 2 else "Continuing with code {0}\n".format(code))
    
    #Parses args array from user, returning dict of filepaths (using std where appropriate)
    #.\Data\(Windows format) 2016 10 29 valid data.txt is default input file
    def parseArgs(self):
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', default=self.input_file)
        parser.add_argument('-e', default=self.error_file)
        parser.add_argument('-s', default=self.suspense_file)
        parser.add_argument('-m', default=self.markup_file)
        parser.add_argument('-l', default=self.markup_lang)

        print(parser.parse_args())

