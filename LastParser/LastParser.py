from FileHandler import FileHandler
from DataUtil import DataUtil
from Records.SysCrashRecord import SysCrashRecord
from RegExParser import RegExParser
from JSONEncoder import JSONEncoder
from XMLEncoder import XMLEncoder
from CLIInterface import CLIInterface

if __name__ == "__main__":
    # Default settings
    stdin = '.\Data\(Windows format) 2016 10 29 valid data.txt'
    stdout = './Output/parsed_output.json'
    stderr = './Output/errors.txt'
    lang = 'JSON'

    #Set up CLI interface with defualt options, then parse args into settings
    cli = CLIInterface(stdin, stdout, stderr, lang)
    settings = cli.parseArgs()

    #Set up concrete encoder options, then instantiate version from settings
    encoders = {'JSON': JSONEncoder, 'XML': XMLEncoder}
    #encoder = encoders[settings['l']]()
    encoder = XMLEncoder()

    #Read in the raw data file settings
    rawData = FileHandler.getContentsOfFile(settings['i'])

    #Get/Check/Parse records from raw data
    records = DataUtil.getRecordsFromRawData(rawData)
    records = RegExParser.checkAndParseRecords(records)

    #Encode records
    encoded_records = encoder.encodeFile(records)

    #Write encoded records to output file
    FileHandler.writeDataToFile(settings['m'], encoded_records)