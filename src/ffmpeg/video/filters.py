from ..config import logger
from ..builder import CMDJoiner
from ..handlers import BaseFFMPEG
from ..helpers import runner


class VideoProcess(BaseFFMPEG):

    @runner(force=False)
    def remove_audio(self, output_file=None, force_replace=False):
        logger.info(f"Removing audio from file {self.file_path}")
        _sequence = CMDJoiner(self.cmd)

        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.INPUT(self.file_path).COPY_CODEC.NO_AUDIO.OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner(force=False)
    def take_screenshot(self, output_file, time, force_replace):
        logger.info(f"Extracting one frame at {time}.")

        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.seek(time).INPUT(self.file_path).video_frame(1).video_quality(2).OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner(force=False)
    def extrac_audio(self, stream=None, output_file=None, force_replace=False):
        logger.info(f"Extracting audio form file {self.file_path} with stream index {stream}.")

        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.INPUT(self.file_path).log_level('quiet').audio_quality(0).map(stream).OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner(force=False)
    def reverse_video(self, output_file=None, include_audio=True, force_replace=False):
        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.INPUT(self.file_path)
        if include_audio:
            _sequence.audio_filter('reverse')

        _sequence.video_filter('reverse').OUTPUT_FILE(output_file)
        logger.info(f"Doing reverse of the video {self.file_path}.")
        self.cmd = _sequence.build()

    @runner(force=False)
    def scale(self, filter_string, force_replace, output_file):

        _sequence = CMDJoiner(["ffmpeg"])
        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.INPUT(self.file_path).map(0).video_filter(filter_string).audio_codec('copy').OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner(force=False)
    def convert_to_gif(self, output_file, seek, end, filter_string, force_replace):

        _sequence = CMDJoiner(["ffmpeg"])
        if force_replace:
            _sequence.FORCEFULLY()

        logger.info(f"converting file '{self.file_path}' in gif")
        _sequence.seek(seek).to(end).INPUT(self.file_path)
        _sequence.add_filter(filter_string).video_codec('gif').OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    # @runner(force=False)
    def add_watermark(self, watermark_file, position, scale_factor=None, output_file=None, force_replace: bool = False):
        filter_name = 'watermark'
        if scale_factor is None:
            scale_factor = 0.2

        if output_file is None:
            output_file = f"{self.file_name}_mixed_{self.file_extension}"

        _sequence = CMDJoiner(["ffmpeg"])

        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.INPUT(self.file_path).INPUT(watermark_file).FILTER_COMPLEX(filter_name, scale_factor, position).OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()
        print(f"{self.cmd}")
