from abc import ABC, abstractmethod

class Encoder(ABC):
    """Abstract Encoder, to be implemented with specific encoding protocol"""

    @abstractmethod
    def encodeFile(self, parsed_file):
        pass

