from .metadata import Metadata
from .chapter import ChapterMixing
from ffmpeg.video.filters import VideoProcess
from .base_process import parser


class FFMPEG(Metadata, ChapterMixing, VideoProcess):

    def __init__(self, input_stream: str):
        self.file_path = parser(input_stream)

        super().__init__(self.file_path)
