from FileHandler import FileHandler
from DataUtil import DataUtil
from Records.SysCrashRecord import SysCrashRecord
from RegExParser import RegExParser
import json

if __name__ == "__main__":
    rawData = FileHandler.getContentsOfFile('.\Data\(Windows format) 2016 10 29 valid data.txt')

    records = DataUtil.getRecordsFromRawData(rawData)

    records = RegExParser.checkAndParseRecords([records[96]])

    print(json.dumps(records[0].record))