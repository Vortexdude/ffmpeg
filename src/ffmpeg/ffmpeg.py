from .helpers import validate_time_range
from .metadata import Metadata
from .chapter import ChapterMixing
from ffmpeg.video.filters import VideoProcess
from .base_process import parser
from .config import Config, logger


class FFMPEG(Metadata, ChapterMixing, VideoProcess):

    def __init__(self, input_stream: str):
        self.file_path = parser(input_stream)

        super().__init__(self.file_path)


    def convert_to_gif(self, output_file=None, seek: str = None, end: str = None, fps: int = None, width: int = None, force_replace: bool =False):
        video_duration = self.metadata.get('duration')
        _seek, _end = validate_time_range(video_duration, seek=seek, end=end, max_length=Config.gif_file_length)
        print(f"{_seek=}")
        print(f"{_end=}")