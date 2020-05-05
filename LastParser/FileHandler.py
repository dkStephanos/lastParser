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
