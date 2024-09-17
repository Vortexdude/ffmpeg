from .metadata import Metadata
from .chapter import ChapterMixing
from .video import VideoProcess
from .base_process import BaseProcess
from abc import ABC, abstractmethod

class VideoProcessor(ABC):

    @abstractmethod
    def process(self):
        pass


class FFMPEG(Metadata, ChapterMixing, VideoProcess):

    def __init__(self, input_stream: str):
        self.file_path = input_stream
        if input_stream.startswith("http"):
            self.file_path = BaseProcess(input_stream).run()

        super().__init__(self.file_path)
