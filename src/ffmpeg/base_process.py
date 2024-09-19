import re
from .config import logger
from .builder import CMDJoiner
from ffmpeg.exceptions import errors
from .helpers import runner, id_generator


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

    @runner(force=False)
    def download(self, output_file=None):
        joiner = CMDJoiner(['ffmpeg']).INPUT(self.url).codec('copy').audio_bitstream("aac_adtstoasc")
        self.cmd = joiner.OUTPUT_FILE(output_file).build()


def parser(file) -> str:
    """
    Download the file depending upon the extension of the file
    later add the logic for autosave 
    :param file:
    :type file:
    :return:
    :rtype:
    """
    _url_pattern = r'https:\/\/[^\s]+?\.(mp3|mp4|m3u8|flv|mkv|jpg|png|jpeg)'
    matches = re.findall(_url_pattern, file)
    for match in matches:
        if match == 'm3u8':
            logger.info("Extracting HLS stream file.")
            return BaseProcess(file).run()
    return file
