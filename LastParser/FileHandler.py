class FileHandler(object):
    
    @staticmethod
    def openFileFromPath(filepath):
        file = open(filepath)

        return file

    @staticmethod
    def getContentsOfFile(filepath):
        file = open(filepath)
        data = file.read()

        return data

    @staticmethod
    def writeDataToFile(filepath, data):
        file = open(filepath, "w+")

        for row in data:
            file.write(row)

        return 0

    @staticmethod
    def writeLineToFile(filepath, line):
        file = open(filepath, "w+")

        file.write(line)

        return 0