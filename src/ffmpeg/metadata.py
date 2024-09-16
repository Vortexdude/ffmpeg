import json
from subprocess import run
from .handlers import BaseFFMPEG
from .builder import CMDJoiner
from .helpers import FFMpegHelper, runner

class Metadata(BaseFFMPEG):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.metadata = self.extract_meta()
        self.audio_streams = FFMpegHelper.format_stream(streams=self.metadata.get('streams'), _type='audio')
        self.video_streams = FFMpegHelper.format_stream(streams=self.metadata.get('streams'), _type='video')

    @runner
    def _get_metadata(self) -> run:
        cmd_builder = CMDJoiner(cmd=["ffprobe"]).log_level("quiet").INPUT_FILE(self.file_path).print_format("json").DISPLAY_STREAM.DISPLAY_CHAPTERS
        self.cmd = cmd_builder.build()
        return {
            'duration': '00:05:12',
            'video_streams': [{'index': 0, 'codec': 'h264', 'resolution': '1920x1080'}],
            'audio_streams': [{'index': 1, 'codec': 'aac', 'language': 'en'}]
        }

    def extract_meta(self) -> dict:
        data = self._get_metadata()
        self.cmd = ["ffmpeg"]
        return json.loads(data)
