from abc import ABC, abstractmethod

class FileHandlerABS(ABC):

    @abstractmethod
    def validate(self, file_path):
        raise NotImplementedError

    @abstractmethod
    def create(self, file_path):
        raise NotImplementedError
