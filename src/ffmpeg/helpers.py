import os
import random
import string
import subprocess as sp
from .config import logger
from functools import wraps
from typing import Any, List, Dict
from ffmpeg.exceptions import errors

def runner(force=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            force_replace = kwargs.get('force_replace', False) or force

            if force_replace:
                logger.info("force is enable")

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
                    logger.warning("File already exists overwriting the file")

            output = sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
            self._reset()

        return wrapper
    return decorator


class FFMpegHelper:

    @staticmethod
    def format_stream(streams: List[Dict[str, Any]], _type='audio'):
        """Formats the list of streams based on the type (audio, video, etc.).

        """
        def extract_tag(tag: dict[str, str], key: str, default: str='N/A'):
            return tag.get(key, default)

        _streams = []
        for stream in streams:
            _data = {}
            if stream.get('codec_type') == _type:
                _data = {
                    'index': stream.get('index', "N/A"),
                    'duration': extract_tag(stream.get('tags', {}), "DURATION", "UNKNOWN"),
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


def arg_eval(arg: str) -> tuple[str, str] | None:
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
