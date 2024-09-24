import re
import os
import time
import random
import string
import datetime
import subprocess as sp
from .config import logger
from functools import wraps
from typing import Any, List, Dict, TypeAlias, NewType
from ffmpeg.exceptions import errors

TimeRange: TypeAlias = tuple[str, str]

TimeString = NewType('TimeString', str)

def validate_time_string(time_str: str)-> TimeString:
    pattern = r"^\d{2}:\d{2}:\d{2}$"  # regex for HH:MM:SS pattern
    if re.match(pattern, time_str):
        return TimeString(time_str)
    else:
         raise ValueError(f"Invalid time string format: {time_str}. Expected 'HH:MM:SS'")


def runner(force=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            force_replace = kwargs.get('force_replace', False) or force
            if force_replace:
                logger.info("Force replace is enable.")

            if "ffmpeg" not in self.cmd or "ffprobe" in self.cmd:
                logger.error("Invalid Command")
                raise errors.InvalidCommand

            func(self, *args, **kwargs)

            if 'ffprobe' in self.cmd or func.__name__ == "_get_metadata":
                _metadata = sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
                return _metadata.stdout.decode('utf-8')

            output_file = self.cmd[-1]

            if os.path.exists(output_file):
                if not force_replace:
                    logger.error(f"File '{output_file}' already exists you can overwrite the file by args.")
                    raise errors.FileAlreadyExists(file=output_file)
                else:
                    logger.warning(f"File '{output_file}' already exists overwriting the file")

            sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
            self._reset()

        return wrapper
    return decorator


class FFMpegHelper:

    @staticmethod
    def format_stream(streams: List[Dict[str, Any]], _type='audio'):
        """Formats the list of streams based on the type (audio, video, etc.).

        """

        def extract_tag(tag: dict[str, str], key: str, default: str = 'N/A'):
            return tag.get(key, default)

        _streams = []
        for stream in streams:
            _data = {}
            if stream.get('codec_type') == _type:
                _data = {
                    'index': stream.get('index', "N/A"),
                    'duration': stream.get('duration', "UNKNOWN"),
                }

                if _type == 'audio':
                    _data['name'] = extract_tag(stream.get('tags', {}), "language", "UNKNOWN")

                title = extract_tag(stream.get('tags', {}), "title", "Untitled")

                if title != 'Untitled':
                    _data['title'] = title

                _streams.append(_data)
        return _streams

    @staticmethod
    def generate_chapter_filename(input_file: str, chapter: dict) -> str:
        """
        Generates a filename for a chapter based on its start time, end time, and title.

        :param input_file: given file name
        :type input_file:
        :param chapter: A dictionary containing chapter information.
        :return: Generated filename for the chapter.
        """
        file, extension = os.path.splitext(os.path.basename(input_file))
        start_time = int(float(chapter['start_time']))
        end_time = int(float(chapter['end_time']))
        title = chapter['tags']['title'].replace(" ", "_")
        return f"{file}_{start_time}-{end_time}_{title}{extension}"

    @staticmethod
    def dimension_arg_eval(arg: str) -> tuple[str, str] | None:
        """
        Evaluate the width and height from arg string as per the given format
        1. w=200:h=100
        2. 200:100
        3. 200x100 or 200X100
        :param arg:
        :type arg:
        :return:
        :rtype:
        """
        width = None
        height = None

        if "x" in arg.lower():
            width, height = arg.lower().split("x")

        if ":" in arg:
            _w, _h = arg.split(":")
            if "w" in _w.lower() and "h" in _h.lower():
                if "=" in _w.lower() and "=" in _h.lower():
                    width = _w.split("=")[1]
                    height = _h.split("=")[1]
            else:
                width, height = _w, _h

        return width, height


def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return "".join(random.choice(chars) for _ in range(size))


class TConverter:
    FORMAT: str = "%H:%M:%S"

    @classmethod
    def to_string(cls, seconds: int | float) -> str:
        """
        Converts seconds into formatted string with hour:minutes:seconds
        :param seconds:
        :type seconds:
        :return:
        :rtype:
        """
        return time.strftime(cls.FORMAT, time.gmtime(seconds))

    @classmethod
    def to_seconds(cls, data: str) -> int | float:
        """
        Covert the string into total seconds like 00:10:00 into 600 seconds
        :param data:
        :type data:
        :return:
        :rtype:
        """
        x = time.strptime(data, cls.FORMAT)
        return datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()


def validate_time_range(video_duration: str,
                        seek: TimeString = None,
                        end: TimeString = None,
                        max_length: int = 10) -> TimeRange:

    video_runtime = TConverter.to_seconds(validate_time_string(video_duration))
    if seek is None and end is None:
        _seek = 3.0
        _end = float(_seek + max_length)
    else:
        if seek is None:
            _end = TConverter.to_seconds(validate_time_string(end))
            _seek = max(_end - max_length, 0)

        elif end is None:
            _seek = TConverter.to_seconds(validate_time_string(seek))
            _end = _seek + max_length

        else:
            _seek = TConverter.to_seconds(validate_time_string(seek))
            _end = TConverter.to_seconds(validate_time_string(end))

    if _seek > video_runtime and _end > video_runtime:
        logger.warning("Seek and end time are beyond the video length.")
        _seek = max(video_runtime - max_length, 0)
        _end = video_runtime

    elif _seek > video_runtime:
        logger.warning("Seek is greater than the length of the video")
        _seek = max(video_runtime - max_length, 0)

    elif _end > video_runtime:
        logger.warning("End is greater than the length of the video")
        _end = video_runtime

    return TConverter.to_string(_seek), TConverter.to_string(_end)


class FilterUtils:
    VIDEO_KEY: str = "video"
    AUDIO_KEY: str = 'audio'
    IMAGE_KEY: str = 'image'
    VIDEO_EXTENSIONS = ['.webm', '.mkv', '.flv', '.mov', '.avi', '.mp4', '.mpeg', '.m4v', '.3gp']
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', ".png", "webm", ".gif", ".svg", "webp"]


    @staticmethod
    def _wh_string_generator(scaling_factor: float = None):
        _image_width = ""
        _image_height = "oh*mdar"  # output_height X maintain the display aspect ratio
        if scaling_factor:
            _image_width = f"ih*{str(scaling_factor)}"  # input height x 0.2 or 20% of video's height

        return f"{_image_height}:{_image_width}"

    @classmethod
    def _overlay_filter_string(cls, position: str, padding: int = None):
        _width = ""
        _height = ""
        _available_positions = ['top_left', "top_right", "bottom_left", "bottom_right", "centre"]
        if position not in _available_positions:
            raise ValueError(f"Unsupported position for now : {_available_positions}")

        _init_string = f"[{cls.VIDEO_KEY}][{cls.IMAGE_KEY}]overlay="
        if position == "top_left":
            _width = "0"
            _height = "0"

        elif position == 'top_right':
            _width = "(main_w-overlay_w)"
            _height = "0"

        elif position == 'bottom_left':
            _width = "0"
            _height = "(main_h-overlay_h)"

        elif position == 'bottom_right':
            _width = "(main_w-overlay_w)"
            _height = "(main_h-overlay_h)"

        elif position == 'centre':
            _width = "(main_w-overlay_w)/2"
            _height = "(main_h-overlay_h)/2"

        if padding:
            if _width != "0":
                _width = f"{_width}-{str(padding)}"
            else:
                _width = padding
            if _height != "0":
                _height = f"{_height}-{str(padding)}"
            else:
                _height = padding

        return _init_string + f"{_width}:{_height}"


    @classmethod
    def create_filter_string(cls, total_inputs, scaling_factor, filter_name, position: str = 'top_left', padding=None):
        key_mapping: dict = {}
        for idx, _input in enumerate(total_inputs):
            _extension = os.path.splitext(_input)[1]
            if _extension in cls.VIDEO_EXTENSIONS:
                key_mapping[cls.VIDEO_KEY] = idx

            elif _extension in cls.IMAGE_EXTENSIONS:
                key_mapping[cls.IMAGE_KEY] = idx

            else:
                key_mapping[f"input_{idx}"] = idx

        video_key = key_mapping[cls.VIDEO_KEY]
        image_key = key_mapping[cls.IMAGE_KEY]
        wh_string = cls._wh_string_generator(scaling_factor)

        if filter_name == "scale2ref":
            return f"[{image_key}][{video_key}]scale2ref={wh_string}[{cls.IMAGE_KEY}][{cls.VIDEO_KEY}]"

        elif filter_name == "overlay":
            if padding is None:
                padding = 30
            return cls._overlay_filter_string(position=position, padding=padding)

        else:
            raise ValueError("Unsupported filter, Get some Help!")



class FFMPegFilterBuilder:
    def __init__(self):
        self.commands = []
        self.sub_filters = []

    def add_input(self, value):
        self.commands.append(f"[{value}]")
        return self

    def format_filter(self, format_type='rgba'):
        self.sub_filters.append(f"format={format_type}")
        return self

    def scale2ref(self, width="oh*mdar", height="ih"):
        self.sub_filters.append(f"scale2ref={width}:{height}")
        return self

    def overlay(self, width="(main_w-overlay_w)/2", height="(main_h-overlay_h)/2"):
        self.sub_filters.append(f"overlay={width}:{height}")
        return self

    def color_channel_mixer(self, alpha=0.3):
        self.sub_filters.append(f"colorchannelmixer=aa={alpha}")
        return self

    def _setter(self):
        if self.sub_filters:
            self.commands.append(",".join(self.sub_filters))
            self.sub_filters = []

    def link_stream(self, output_stream):
        self._setter()
        self.commands.append(f"[{output_stream}]")
        return self

    def build(self):
        self._setter()
        return "".join(self.commands)

    def reset(self):
        self.commands = []
        self.sub_filters = []
