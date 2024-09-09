from ffmpeg.constants import DefaultProperties, Flags, Filters
from ffmpeg.handlers import runner
from ffmpeg.abstractions import FilterMixingABS


class Filter(FilterMixingABS, DefaultProperties):

    @runner
    def remove_audio(self, force_replace: bool = False):
        self.input = self.input_file
        self.common_codec = Flags.COPY
        self.options = Flags.NO_AUDIO
        output_file = f"{self.file_name}_no_audio{self.file_extension}"
        self.cmd.extend(self.input + self.common_codec + self.options + [output_file])

    @runner
    def take_screenshot(self, time=None):
        if time is None:
            time = "00:10:00"
        self.input = self.input_file
        self.seek = time
        self.video_frames = '1'
        self.video_quality = '2'

        output_file = f"{self.file_name}_at_{time}.jpg"
        self.cmd.extend(self.seek + self.input + self.video_frames + self.video_quality + [output_file])

    @runner
    def get_audio(self, stream=None, output_file=None):
        self.input = self.input_file
        self.verbosity = 'quiet'
        self.audio_quality = '0'   #(0-9) highest-lowest

        if stream is None:
            self.map_stream = '0:a:0'
            output_file = output_file if output_file else f"{self.file_name}.mp3"

        else:
            self.map_stream = f"0:{stream['index']}"
            output_file = output_file if output_file else f"{self.file_name}_{stream['tags']['language']}.mp3"

        self.cmd.extend(self.input + self.verbosity + self.audio_quality + self.map_stream + [output_file])

    @runner
    def reverse_video(self, output_file=None, include_audio=True):
        self.input = self.input_file
        filters = []
        self.video_filter = Filters.VIDEO_REVERSE
        filters.extend(self.video_filter)
        if include_audio:
            self.audio_filter = Filters.AUDIO_REVERSE
            filters.extend(self.audio_filter)

        output_file = output_file if output_file else f"{self.file_name}_reversed{self.file_extension}"
        self.cmd.extend(self.input + filters + [output_file])

    def scale(self, size=None, output_file=None):
        output_file = output_file if output_file else f"{self.file_name}_resized{self.file_extension}"
