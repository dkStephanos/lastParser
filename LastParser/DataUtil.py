class DataUtil(object):
    """Helper class for LastParser to encapsulate basic data handling methods"""

    @staticmethod
    def getRecordsFromRawData(rawData):
        records = rawData.split("\n")

        return records