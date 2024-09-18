from ..config import logger
from ..helpers import runner, arg_eval
from ..handlers import BaseFFMPEG
from ..builder import CMDJoiner


class VideoProcess(BaseFFMPEG):

    @runner(force=False)
    def remove_audio(self, output_file=None, force_replace=False):
        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        logger.info(f"Removing audio from file {self.file_path}")
        output_file = output_file if output_file else f"{self.file_name}_no_audio{self.file_extension}"

        _sequence.INPUT(self.file_path).COPY_CODEC.NO_AUDIO.OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner(force=False)
    def take_screenshot(self, time=None, force_replace=False):
        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        FILE_EXTENSION = ".jpg"
        if time is None:
            time = "00:10:00"
        output_file = f"{self.file_name}_at_{time}{FILE_EXTENSION}"
        logger.info(f"Extracting one frame at {time}.")
        _sequence.seek(time).INPUT(self.file_path).video_frame(1).video_quality(2).OUTPUT_FILE(output_file)

        self.cmd = _sequence.build()

    @runner(force=False)
    def extrac_audio(self, stream=None, output_file=None, force_replace=False):
        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        FILE_EXTENSION = ".mp3"
        if stream is None:
            _stream = "0:a:a"
            output_file = output_file if output_file else f"{self.file_name}_0_A_0{FILE_EXTENSION}"
        else:
            _stream = f"0:{stream['index']}"
            output_file = output_file if output_file else f"{self.file_name}_{stream['name']}{FILE_EXTENSION}"

        logger.info(f"Extracting audio form file {self.file_path} with stream index {_stream}.")
        _sequence.INPUT(self.file_path).log_level('quiet').audio_quality(0).map(_stream).OUTPUT_FILE(output_file)

        self.cmd = _sequence.build()

    @runner(force=False)
    def reverse_video(self, output_file=None, include_audio=True, force_replace=False):
        _sequence = CMDJoiner(self.cmd)
        if force_replace:
            _sequence.FORCEFULLY()

        output_file = output_file if output_file else f"{self.file_name}_reverse{self.file_extension}"
        _sequence.INPUT(self.file_path)
        if include_audio:
            _sequence.audio_filter('reverse')

        _sequence.video_filter('reverse').OUTPUT_FILE(output_file)
        logger.info(f"Doing reverse of the video {self.file_path}.")
        self.cmd = _sequence.build()

    @runner(force=False)
    def scale(self, arg: str = None, *, width: int = None, height: int = None, factor: int = None,
              force_replace: bool = False):

        _sequence = CMDJoiner(["ffmpeg"])
        if force_replace:
            _sequence.FORCEFULLY()

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
        logger.info(f"Scaling file {self.file_path} in to {width}X{height}.")
        _sequence.INPUT(self.file_path).map(0).video_filter(_filter).audio_codec('copy').OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()

    @runner(force=False)
    def convert_to_gif(self, output_file=None, fps: int = None, width: int = None, force_replace: bool =False):
        _sequence = CMDJoiner(["ffmpeg"])
        if force_replace:
            _sequence.FORCEFULLY()

        _file_extension = '.gif'
        if not fps:
            fps = 10

        if not width:
            width = 320

        if not output_file:
            output_file = f"{self.file_name}_image{_file_extension}"

        _filter = {'fps': str(fps), 'scale': f'{str(width)}:-1:flags=lanczos'}

        logger.info(f"converting file {self.file_name} in gif")
        _sequence.INPUT(self.file_path).add_filter(_filter).video_codec('gif').OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()
