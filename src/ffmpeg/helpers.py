import re
import time
import random
import string
import datetime
import subprocess as sp
from pathlib import Path
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

            if 'ffprobe' in self.cmd:
                _metadata = sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
                return _metadata.stdout.decode('utf-8')

            output_file = Path(self.cmd[-1])
            if output_file.exists():
                if not force_replace:
                    logger.error(f"File '{output_file}' already exists you can overwrite the file by args.")
                    raise errors.FileAlreadyExists(file=output_file)
                else:
                    logger.warning(f"File '{output_file}' already exists overwriting the file")

            output = sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
            print(output.stdout.decode('utf-8'))
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
    def generate_chapter_filename(input_file: Path, chapter: dict) -> str:
        """
        Generates a filename for a chapter based on its start time, end time, and title.

        :param input_file: given file name
        :type input_file:
        :param chapter: A dictionary containing chapter information.
        :return: Generated filename for the chapter.
        """
        if isinstance(input_file, Path):
            input_file = Path(input_file)

        start_time = int(float(chapter['start_time']))
        end_time = int(float(chapter['end_time']))
        title = chapter['tags']['title'].replace(" ", "_")
        return f"{input_file.stem}_{start_time}-{end_time}_{title}{input_file.suffix}"

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

def time_extractor(expression, time) -> int:
    x = re.match(expression, time)
    hour = int(x.group(1))
    minutes = int(x.group(2))
    seconds = int(x.group(3))
    total_minutes = (hour * 60) + minutes
    total_seconds = (total_minutes * 60) + seconds
    return total_seconds * 1000
