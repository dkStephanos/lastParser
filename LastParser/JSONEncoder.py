import json
from Encoder import Encoder

class JSONEncoder(Encoder):
    
    @staticmethod
    def encodeFile(parsed_records):
        encoded_records = {'sessions': ''}

        for record in parsed_records:
            encoded_records['sessions'] += json.dumps({'session': record.record})

        return json.dumps(encoded_records)


