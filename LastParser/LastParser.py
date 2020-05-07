import sys
from FileHandler import FileHandler
from DataUtil import DataUtil
from Records.SysCrashRecord import SysCrashRecord
from RegExParser import RegExParser
from JSONEncoder import JSONEncoder
from XMLEncoder import XMLEncoder
from CLIInterface import CLIInterface
from ErrorHandler import ErrorHandler

if __name__ == "__main__":
    # Default settings
    stdin = '.\Data\(Windows format) 2016 10 29 erroneous data.txt'
    stdout = './Output/parsed_output.json'
    stderr = './Output/errors.txt'
    lang = 'JSON'

    try:
        #Set up CLI interface with defualt options, then parse args into settings
        cli = CLIInterface(stdin, stdout, stderr, lang)
        settings = cli.parseArgs()

        ErrorHandler.verifyInputFile(settings)    

        #Set up concrete encoder options, then instantiate version from settings
        encoders = {'JSON': JSONEncoder, 'XML': XMLEncoder}
        encoder = encoders[settings['l']]()

        #Read in the raw data file settings
        rawData = FileHandler.getContentsOfFile(settings['i'])

        #Get/Check/Parse records from raw data
        records = DataUtil.getRecordsFromRawData(rawData)
        [records, unparsed_records, errors] = RegExParser.checkAndParseRecords(records)

        #Write errors and unparsable records to error/suspense files
        FileHandler.writeDataToFile(settings['s'], unparsed_records)
        FileHandler.writeDataToFile(settings['e'], errors)

        #Encode records
        encoded_records = encoder.encodeFile(records)

        #Write encoded records to output file
        FileHandler.writeDataToFile(settings['m'], encoded_records)

    except:
        print(sys.exc_info())
        sys.exit(sys.exc_info()[1])