from dicttoxml import dicttoxml
from Encoder import Encoder
from xml.etree.ElementTree import tostring

class XMLEncoder(Encoder):
    
    @staticmethod
    def encodeFile(parsed_records):
        encoded_records = {'sessions': []}

        for record in parsed_records:
            encoded_records['sessions'].append({'session': record.record})

        return dicttoxml(encoded_records).decode('utf-8')


