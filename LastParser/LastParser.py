from FileHandler import FileHandler
from DataUtil import DataUtil
from Records.SysCrashRecord import SysCrashRecord
from RegExParser import RegExParser
from JSONEncoder import JSONEncoder
from CLIInterface import CLIInterface

if __name__ == "__main__":
    stdin = '.\Data\(Windows format) 2016 10 29 valid data.txt'
    stdout = './Output/parsed_output.json'
    stderr = './Output/errors.txt'
    lang = 'JSON'

    encoders = {'JSON': JSONEncoder.encodeFile}

    cli = CLIInterface(stdin, stdout, stderr, lang)

    settings = cli.parseArgs()

    #print(sys.argv)

    rawData = FileHandler.getContentsOfFile(stdin)

    records = DataUtil.getRecordsFromRawData(rawData)
    records = RegExParser.checkAndParseRecords(records)

    encoded_records = encoders[settings['l']](records)

    FileHandler.writeDataToFile("Output/parsed_output.json", encoded_records)