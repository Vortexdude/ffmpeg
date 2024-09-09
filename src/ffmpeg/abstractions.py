from abc import ABC, abstractmethod
import os

class FileHandler(ABC):
    """
    Abstract base class for handling file operations.
    """

    @abstractmethod
    def validate(self, path: str):
        """
        Abstract method to validate if a file or directory exists.

        :param path: Path to validate.
        :return: Validated path.
        """
        pass


    def create(self, path: str):
        """
        Abstract method to create a directory if it does not exist.

        :param path: Directory path to create.
        """
        pass


class ChaptersMixingABS(ABC):
    """
    Abstract base class for processing video files.
    """
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.output_file = None
        self.cmd = ['ffmpeg']

    @abstractmethod
    def split(self, chapters: list) -> None:
        """
        Abstract method to split the video into chapters.
        """
        pass

class FilterMixingABS(ABC):
    """
    Abstract bas class for provide the input file
    """

    def __init__(self, input_file: str):
        self.cmd = ['ffmpeg']
        self.input_file = input_file
        self.file_name, self.file_extension = os.path.splitext(os.path.basename(self.input_file))
        self.output_file = None
        self._audio_streams = []
        self._video_streams = []
        self._subtitles = []
