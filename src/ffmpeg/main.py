from ffmpeg.filters import Filter
from ffmpeg.metadata import MetaData
from ffmpeg._chapters import ChapterMixing

class FFMPEG(MetaData):

    def __init__(self, input_file, *, file_handler=None):
        self.file_handler = file_handler
        self.input_file = input_file
        self.cmd = []
        super().__init__(input_file, file_handler=file_handler)
        super().get_metadata()

    def split_chapter(self, chapters: list):
        ChapterMixing(self.input_file).split(chapters)

    def remove_audio(self, force_replace=False):
        Filter(self.input_file).remove_audio()

    def take_screenshot(self, time=None):
        Filter(self.input_file).take_screenshot(time)

    def extrac_audio(self, stream=None, output_file=None):
        Filter(self.input_file).get_audio(stream, output_file)

    def reverse_video(self, output_file=None):
        Filter(self.input_file).reverse_video(output_file)

    def scale(self, force=True):
        Filter(self.input_file).scale(self.width, self.height)
