import sys

class CLIInterface(object):
    stdin = '.\Data\(Windows format) 2016 10 29 valid data.txt'
    stdout = './Output/records.txt'
    stderr = '.\Output\errors.txt'

    #Logs status and code to screen
    @staticmethod
    def log(status, code):
        print(status + "Exiting with code 2\n" if code == 2 else "Continuing with code {0}\n".format(code))
    
    #Parses args array from user, returning dict of filepaths (using std where appropriate)
    #.\Data\(Windows format) 2016 10 29 valid data.txt is default input file
    def parseArgs(args):
        settings = {'input_file': ".\Data\(Windows format) 2016 10 29 valid data.txt",
                    'markup_file': "parsed_output.json", 'error_file': "errors.txt",
                    'suspense_file': "errors.txt", 'language': 'JSON'}
        #parse args


        return settings

