from .config import logger
from .helpers import runner, id_generator
from .builder import CMDJoiner
from ffmpeg.exceptions import errors


class BaseProcess:

    def __init__(self, url: str):
        self.url = self._validate_stream_file(url)
        self.cmd = ['ffmpeg']
        self.file_path = None

    def _reset(self):
        self.cmd = ["ffmpeg"]

    @staticmethod
    def _validate_stream_file(url: str) -> str:
        if not url.startswith("http"):
            raise errors.ProtocolNotDefined

        if not url.endswith("m3u8"):
            raise errors.URLStreamError

        return url

    def run(self, output_file=None) -> str:
        if not output_file:
            output_file = f"{id_generator()}.mp4"

        self.download(output_file)
        return output_file  # set the input for other filter

    @runner
    def download(self, output_file=None):
        joiner = CMDJoiner(['ffmpeg']).INPUT(self.url).codec('copy').audio_bitstream("aac_adtstoasc")
        self.cmd = joiner.OUTPUT_FILE(output_file).build()
