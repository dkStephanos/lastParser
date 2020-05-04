from abc import ABC, abstractmethod

class Record(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    @abstractmethod
    def set_record(self, record):
        this.record = record

    @abstractmethod
    def get_record(self, record):
        return this.record

