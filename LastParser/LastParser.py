from FileHandler import FileHandler
from DataUtil import DataUtil
from Records.SysCrashRecord import SysCrashRecord

if __name__ == "__main__":
    rawData = FileHandler.getContentsOfFile('.\Data\(Windows format) 2016 10 29 valid data.txt')

    records = DataUtil.getRecordsFromRawData(rawData)

    print(records[0])