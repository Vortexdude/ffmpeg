import os

from ffmpeg.constants import DefaultProperties
from ffmpeg.handlers import runner
from ffmpeg import exceptions
from ffmpeg.config import config
from ffmpeg.handlers import LocalFileHandler
from ffmpeg.abstractions import ChaptersMixingABS


class ChapterMixing(ChaptersMixingABS, DefaultProperties):
    OUTPUT_DIR = config.OUTPUT_DIR

    def _generate_filename(self, chapter: dict) -> str:
        """
        Generates a filename for a chapter based on its start time, end time, and title.

        :param chapter: A dictionary containing chapter information.
        :return: Generated filename for the chapter.
        """
        file, extension = os.path.splitext(os.path.basename(self.input_file))
        start_time = int(float(chapter['start_time']))
        end_time = int(float(chapter['end_time']))
        title = chapter['tags']['title'].replace(" ", "_")
        return f"{file}_{start_time}-{end_time}_{title}{extension}"

    def split(self, chapters=None, force_recreation_chapter=False) -> None:
        """
        Splits the video into separate files, one for each chapter using FFmpeg.
        """
        if chapters is None:
            chapters = []

        if not chapters:
            raise exceptions.NoChapterProvided()

        LocalFileHandler().create(self.OUTPUT_DIR)
        for chapter in chapters:
            self.split_chapter(chapter, force_recreation_chapter=force_recreation_chapter)

    @runner
    def split_chapter(self, chapter: dict, force_recreation_chapter=False):
        self.input = self.input_file
        self.audio_codec = 'copy'
        self.video_codec = 'copy'
        self.seek = chapter['start_time']
        self.to = chapter['end_time']
        output_file = os.path.join(self.OUTPUT_DIR, self._generate_filename(chapter))
        self.cmd = self.cmd + self.input + self.audio_codec + self.video_codec + self.seek + self.to + [output_file]
