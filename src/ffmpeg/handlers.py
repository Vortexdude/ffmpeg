import os
from pathlib import Path
from .base import FileHandlerABS


class BaseFFMPEG:
    def __init__(self, file_path: str):
        self.cmd = ['ffmpeg']
        self.file_path = FileHandler().validate(file_path)
        self.file_name = self.file_path.stem
        self.file_extension = self.file_path.suffix
        self.metadata: dict = {}

    def _reset(self):
        self.cmd = ["ffmpeg"]


class FileHandler(FileHandlerABS):

    def validate(self, file_path) -> Path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not exists {file_path}")
        return path

    def create(self, file_path):
        if not os.path.exists(file_path):
            # check for the directory also
            os.makedirs(file_path)
