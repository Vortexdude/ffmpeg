import json
from subprocess import run
from .builder import CMDJoiner
from .handlers import BaseFFMPEG
from .helpers import FFMpegHelper, runner, TConverter


class Metadata(BaseFFMPEG):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.metadata = self.extract_meta()
        self.audio_streams = FFMpegHelper.format_stream(streams=self.metadata.get('streams'), _type='audio')
        self.video_streams = FFMpegHelper.format_stream(streams=self.metadata.get('streams'), _type='video')
        self.metadata['type'] = self._filter_type()
        self.metadata['duration'] = TConverter.to_string(float(self.video_streams[0]['duration']))

    def _filter_type(self) -> str:
        media_format = self.metadata.get('format')
        format_name = media_format.get('format_name')
        if "mp3" in format_name:
            return "audio"
        if 'mp4' in format_name or 'mov' in format_name:
            return "video"
        if 'image2' in format_name:
            return "image"


    @runner()
    def _get_metadata(self) -> run:
        _sequence = CMDJoiner(['ffprobe'])
        _sequence.log_level("quiet").INPUT(self.file_path).print_format("json")
        self.cmd = _sequence.SHOW_FORMAT.SHOW_STREAM.SHOW_CHAPTERS.build()
        return {
            'duration': '00:05:12',
            'video_streams': [{'index': 0, 'codec': 'h264', 'resolution': '1920x1080'}],
            'audio_streams': [{'index': 1, 'codec': 'aac', 'language': 'en'}]
        }

    def extract_meta(self) -> dict:
        data = self._get_metadata()
        self.cmd = ["ffmpeg"]
        return json.loads(data)
