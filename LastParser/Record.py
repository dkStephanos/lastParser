from abc import ABC, abstractmethod

class Record(ABC):
    def __init__(self, record):
        self.record = record
        super().__init__()
    
    def set_record(self, record):
        self.record = record

    def get_record(self):
        return self.record

