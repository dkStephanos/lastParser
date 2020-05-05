import json
from Encoder import Encoder

class JSONEncoder(Encoder):
    
    def encodeFile(self, parsed_file):
        return json.dump(parsed_file)


