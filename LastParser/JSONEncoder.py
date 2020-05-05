import json
from Encoder import Encoder

class JSONEncoder(Encoder):
    
    @staticmethod
    def encodeFile(parsed_records):
        encoded_records = []

        for record in parsed_records:
            encoded_records.append(json.dumps(record.record))

        return encoded_records


