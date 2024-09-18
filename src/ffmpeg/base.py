from abc import ABC, abstractmethod

class FileHandlerABS(ABC):

    @abstractmethod
    def validate(self, file_path):
        raise NotImplementedError

    @abstractmethod
    def create(self, file_path):
        raise NotImplementedError


class VideoProcessorABS(ABC):

    @abstractmethod
    def remove_audio(self, *args, force_replace=False, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def take_screenshot(self, *args, force_replace=False, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def convert_to_gif(self, *args, force_replace=False, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def reverse_video(self, *args, force_replace=False, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def scale(self, *args, force_replace=False, **kwargs):
        raise NotImplementedError
