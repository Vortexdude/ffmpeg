import os
import json
import subprocess as sp
from functools import wraps
from ffmpeg import exceptions
from ffmpeg.logger import logger
from ffmpeg.abstractions import FileHandler
from ffmpeg.constants import Columns, Filters, Flags

# blaster800

def runner(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        output_file = self.cmd[-1]

        if func.__name__ == 'metadata':
            _metadata = sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
            return json.loads(_metadata.stdout.decode('utf-8'))

        if os.path.exists(output_file):
            if "force_recreation_chapter" in kwargs.keys():
                logger.error(f"Chapter '{output_file}' already exists. Please delete the existing file first.")
                raise exceptions.ChapterAlreadyExistsException()

            raise exceptions.FileAlreadyExists(output_file)

        output = sp.run(self.cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
        logger.debug(f"Created the file at {output_file}")
        self.cmd = ['ffmpeg']

    return wrapper



class LocalFileHandler(FileHandler):
    def validate(self, path: str):
        if not os.path.exists(path):
            raise exceptions.FileNotFound(file=path)
        return path

    def create(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
            logger.debug(f"Directory '{path}' created successfully.")


class BaseMetadata:

    def __init__(self, input_file, *, file_handler=None):
        self.file_handler = LocalFileHandler() if not file_handler else file_handler()
        self.input_file = self.file_handler.validate(input_file)
        self.chapters = None
        self.streams = None
        self.width = None
        self.height = None
        self.cmd = []

    @runner
    def metadata(self, columns=None):
        columns = columns if columns else [Columns.STREAMS, Columns.CHAPTERS]
        self.cmd = ["ffprobe"] + ["-v", "quiet"] + [Flags.FORMATTER, Filters.JSON] + columns + [self.input_file]
