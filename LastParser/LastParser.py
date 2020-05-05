from FileHandler import FileHandler
from DataUtil import DataUtil
from Records.SysCrashRecord import SysCrashRecord
from RegExParser import RegExParser
import json

if __name__ == "__main__":
    rawData = FileHandler.getContentsOfFile('.\Data\(Windows format) 2016 10 29 valid data.txt')

    records = DataUtil.getRecordsFromRawData(rawData)
    records[-1]

    records = RegExParser.checkAndParseRecords(records)

    print(len(records))
    print('Done')