from ..config import logger
from ..helpers import runner, arg_eval
from ..handlers import BaseFFMPEG
from ..builder import CMDJoiner


class VideoProcess(BaseFFMPEG):

    @runner
    def remove_audio(self, output_file=None, force_replace=False):
        logger.info(f"Removing audio from file '{self.file_path}'")
        output_file = output_file if output_file else f"{self.file_name}_no_audio{self.file_extension}"
        _sequence = CMDJoiner(self.cmd).INPUT(self.file_path).COPY_CODEC.NO_AUDIO.OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner
    def take_screenshot(self, time=None):
        FILE_EXTENSION = ".jpg"
        if time is None:
            time = "00:10:00"
        output_file = f"{self.file_name}_at_{time}{FILE_EXTENSION}"
        self.cmd = CMDJoiner().seek(time).INPUT(self.file_path).video_frame(1).video_quality(2).OUTPUT_FILE(output_file).build()
        logger.info(f"Extracting one frame at {time}")

    @runner
    def extrac_audio(self, stream=None, output_file=None):
        FILE_EXTENSION = ".mp3"
        _sequence = CMDJoiner().INPUT(self.file_path).log_level('quiet').audio_quality(0)
        if stream is None:
            _stream = "0:a:a"
            output_file = output_file if output_file else f"{self.file_name}_0_A_0{FILE_EXTENSION}"
        else:
            _stream = f"0:{stream['index']}"
            output_file = output_file if output_file else f"{self.file_name}_{stream['name']}{FILE_EXTENSION}"

        self.cmd = _sequence.map(_stream).OUTPUT_FILE(output_file).build()


    @runner
    def reverse_video(self, output_file=None, include_audio=True):
        output_file = output_file if output_file else f"{self.file_name}_reverse{self.file_extension}"
        _sequence = CMDJoiner().INPUT(self.file_path)
        if include_audio:
            _sequence.audio_filter('reverse')

        self.cmd = _sequence.video_filter('reverse').OUTPUT_FILE(output_file).build()

    @runner
    def scale(self, arg: str =None, * , width: int=None, height: int=None, factor: int = None):
        _filter = "scale="
        if arg:
            _w, _h = arg_eval(arg)
            if _w and _h:
                width = _w
                height = _h

        if factor:
            width = f"{factor}*iw"
            height = f"{factor}*ih"

        _filter += f"{width}x{height}"
        output_file = f"{self.file_name}_{width}{self.file_extension}"
        _sequence = CMDJoiner(["ffmpeg"]).INPUT(self.file_path).map(0).video_filter(_filter).audio_codec('copy')
        self.cmd = _sequence.OUTPUT_FILE(output_file ).build()

    @runner
    def convert_to_gif(self, output_file=None, fps: int = None, width: int = None):
        _file_extension = '.gif'
        if not fps:
            fps = 10

        if not width:
            width = 320

        if not output_file:
            output_file = f"{self.file_name}_image{_file_extension}"

        _filter = {'fps': str(fps), 'scale': f'{str(width)}:-1:flags=lanczos'}

        _sequence = CMDJoiner(["ffmpeg"]).INPUT(self.file_path).add_filter(_filter).video_codec('gif')
        self.cmd = _sequence.OUTPUT_FILE(output_file).build()
