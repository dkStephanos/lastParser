from FileHandler import FileHandler

if __name__ == "__main__":
    data = FileHandler.openFileFromPath('.\Data\(Windows format) 2016 10 29 valid data.txt')

    print(data.read())