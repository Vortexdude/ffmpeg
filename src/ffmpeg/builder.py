from .config import logger
from ffmpeg.exceptions import errors

__all__ = ["CMDJoiner"]

SUPPORTED_FILTERS = ['reverse', "scale"]


class BaseClass:
    def __init__(self, cmd=None):
        self._cmd: list = cmd if cmd else ["ffmpeg"]

    @property
    def cmd(self):
        logger.debug(f"Building the command -  {" ".join(self._cmd)}")
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = value


class Constant(BaseClass):

    @property
    def DISPLAY_STREAM(self):
        self.cmd.append("-show_streams")
        return self

    @property
    def DISPLAY_CHAPTERS(self):
        self.cmd.append("-show_chapters")
        return self

    @property
    def NO_AUDIO(self):
        self.cmd.append("-an")
        return self


class Codecs(BaseClass):

    def codec(self, value):
        self.cmd.extend(['-c', value])
        return self

    def audio_codec(self, value):
        self.cmd.extend(["-acodec", value])
        return self

    def video_codec(self, value):
        self.cmd.extend(["-vcodec", value])
        return self

    @property
    def COPY_CODEC(self):
        self.cmd.extend(["-c", "copy"])
        return self


class Filters(BaseClass):
    def add_filter(self, filters):
        filter_string = ",".join([f"{key}={value}" for key, value in filters.items()])
        self.cmd.extend(['-vf', filter_string])
        return self

    def video_filter(self, value):
        if value not in SUPPORTED_FILTERS:
            if 'scale' in value:
                self.cmd.extend(["-filter:v", value])  # or "-vf" is the same
                return self

            raise NotImplementedError

        self.cmd.extend(["-filter:v", value]) # or "-vf" is the same
        return self

    def audio_filter(self, value):
        if value not in SUPPORTED_FILTERS:
            raise NotImplementedError

        self.cmd.extend(["-af", value])
        return self

    def audio_bitstream(self, value):
        self.cmd.extend(["-bsf:a", value])
        return self


class CMDJoiner(Constant, Codecs, Filters):

    def INPUT(self, file):
        self.cmd.extend(["-i", file])
        return self

    def OUTPUT_FILE(self, file):
        self.cmd.append(file)
        return self

    def log_level(self, value):
        self.cmd.extend(["-loglevel", value])
        return self

    def seek(self, time):
        self.cmd.extend(["-ss", time])
        return self

    def to(self, time):
        self.cmd.extend(["-to", time])
        return self

    def print_format(self, value):
        _formats = ["xml", "json", "csv", "sub"]
        if value not in _formats:
            logger.error("invalid option for the supported list")
            raise errors.InvalidOptionError(options=value, optional_values=_formats)

        self.cmd.extend(["-print_format", value])
        return self

    def custom_option(self, *args):
        self.cmd.extend(args)
        return self

    def video_frame(self, number: str):
        if isinstance(number, int):
            number = str(number)

        self.cmd.extend(["-frames:v", number])
        return self

    def video_quality(self, number):
        if isinstance(number, int):
            number = str(number)

        self.cmd.extend(["-q:v", number])
        return self

    def audio_quality(self, value: str):
        if isinstance(value, int):
            value = str(value)

        self.cmd.extend(["-q:a", value])
        return self

    def map(self, value):
        self.cmd.extend(["-map", str(value)])
        return self


    def threads(self, value):
        self.cmd.extend(["-threads", str(value)])
        return self

    def build(self):
        """finalizing the command"""
        logger.info(f"Running the command '{' '.join(self.cmd)}'")
        return self._cmd
