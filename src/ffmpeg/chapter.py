import os
from .config import Config
from .helpers import runner, FFMpegHelper
from .handlers import FileHandler, BaseFFMPEG
from .exceptions import errors
from .config import logger
from .builder import CMDJoiner

class ChapterMixing(BaseFFMPEG):
    def split(self, chapters=None, force_recreation_chapter=False) -> None:
        """
        Splits the video into separate files, one for each chapter using FFmpeg.
        """
        if chapters is None:
            chapters = []

        if not chapters:
            raise errors.NoChapterProvided

        FileHandler().create("outputs")
        for chapter in chapters:

            self.split_chapter(chapter, force_recreation_chapter=force_recreation_chapter)

    @runner
    def split_chapter(self, chapter: dict, force_recreation_chapter=False):
        logger.info(f"Splitting chapter {chapter['id']}")
        output_file = FFMpegHelper.generate_chapter_filename(input_file=self.file_path, chapter=chapter)
        if Config.output_dir:
            output_file = os.path.join(Config.output_dir, output_file)

        self.cmd = CMDJoiner().INPUT(self.file_path).audio_codec('copy').video_codec("copy").seek(chapter['start_time']).to(chapter['end_time']).OUTPUT_FILE(output_file).build()
