from ffmpeg import exceptions
from ffmpeg.logger import logger
from ffmpeg.handlers import BaseMetadata
from ffmpeg.constants import Columns

class MetaData(BaseMetadata):


    def get_metadata(self):
        metadata = self.metadata(columns=[Columns.CHAPTERS, Columns.STREAMS])
        self.chapters = metadata.get('chapters', [])
        self.streams = metadata.get('streams', [])

        if len(self.streams) == 0:
            raise exceptions.NoStreamFound()

        if len(self.chapters) == 0:
            raise exceptions.NoChapterFound()

        audio_streams = [stream for stream in self.streams if stream['codec_type'] == 'audio']
        video_streams = [stream for stream in self.streams if stream['codec_type'] == 'video']
        subtitles = [stream for stream in self.streams if stream['codec_type'] == 'subtitle']

        self.width = video_streams[0]['width']
        self.height = video_streams[0]['height']

        logger.info(f"Found {len(audio_streams)} chapters.")
        logger.info(f"Found {len(audio_streams)} Audio Streams.")
        logger.info(f"Found {len(video_streams)} Video Streams.")
        logger.info(f"Found {len(subtitles)} Subtitles.")
