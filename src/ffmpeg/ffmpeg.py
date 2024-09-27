from .config import Config
from .metadata import Metadata
from .base_process import parser
from ffmpeg.video.chapter import ChapterMixing
from ffmpeg.video.filters import VideoProcess
from ffmpeg.audio.filters import AudioProcessing
from .helpers import TConverter, validate_time_string, FFMpegHelper, validate_time_range


class FFMPEG(Metadata, ChapterMixing, VideoProcess, AudioProcessing):

    def __init__(self, input_stream: str):
        self.file_path = parser(input_stream)

        super().__init__(self.file_path)

    def take_screenshot(self,
                        output_file: str = None,
                        time: str = None,
                        force_replace: bool = False):
        """
        Takes a screenshot from a video at a specified time and saves it to an output file.
        :param output_file:
        :param time:
        :param force_replace:

        output_file : str, optional
            The file path where the screenshot will be saved. If not provided, a default file name will be generated based on the video file name and time.

        time : TimeString, optional
            The timestamp in "HH:MM:SS" format from which to take the screenshot. If not provided, a default time will be used, typically 00:00:03 (3 seconds).

        force_replace : bool, optional, default: False
            If True, it will overwrite the output file if it already exists. If False and the file exists, the function may raise an error or generate a new file name.

        Returns:
        --------
        None
            The screenshot is saved to the specified output file.

        Raises:
        -------
        ValueError
            If the `time` argument is not in the correct "HH:MM:SS" format.

        IOError
            If an issue occurs while saving the screenshot, such as permission issues or disk space.

        Notes:
        ------
        - The video must be loaded into the object instance before calling this method.
        - If `force_replace` is set to False and the output file already exists, the behavior may depend on the implementation (e.g., it could raise an error or create a file with a different name).
        """

        _FILE_EXTENSION = '.jpg'

        video_runtime = TConverter.to_seconds(self.metadata.get('duration'))

        if time is None:
            time = TConverter.to_string(video_runtime // 2)

        time = validate_time_string(time)  # validate the time string

        if output_file is None:
            output_file = f"{self.file_name}_at_{time}{_FILE_EXTENSION}"

        if TConverter.to_seconds(time) >= video_runtime:
            raise ValueError("time range bound error.")

        super().take_screenshot(output_file=output_file, time=time, force_replace=force_replace)

    def remove_audio(self,
                     output_file=None,
                     force_replace=False):
        """
        Removes the audio stream from the video and saves the resulting video file.

        :param output_file:
        :type output_file: str
        :param force_replace:
        :type force_replace: bool
        :return:
        :rtype:

        """
        if output_file is None:
            output_file = f"{self.file_name}_no_audio{self.file_extension}"

        super().remove_audio(output_file=output_file, force_replace=force_replace)

    def extrac_audio(self,
                     stream=None,
                     output_file=None,
                     force_replace=False):
        """
        Extracts the audio stream from the video and saves it as a separate audio file.
        Parameters:
        ----------
        stream : int, optional
            The index of the audio stream to extract. If not provided, the default stream is extracted.

        output_file : str, optional
            The file path where the extracted audio will be saved. If not provided, a default file name will be generated based on the original video file name.

        force_replace : bool, optional, default: False
            If True, it will overwrite the output file if it already exists. If False and the file exists, the function may raise an error or generate a new file name.


        :param stream:
        :type stream:
        :param output_file:
        :type output_file:
        :param force_replace:
        :type force_replace:
        :return:
        :rtype:
        """
        FILE_EXTENSION = ".mp3"
        if stream is None:
            _stream = "0:a:a"
        else:
            _stream = f"0:{stream['index']}"

        if output_file is None:
            output_file = f"{self.file_name}_{_stream[1:3]}{FILE_EXTENSION}"

        super().extrac_audio(stream=_stream, output_file=output_file, force_replace=force_replace)


    def reverse_video(self,
                      output_file=None,
                      include_audio=True,
                      force_replace=False):
        """
        Reverses the video stream and optionally includes the reversed audio.
        Parameters:
        ----------
        output_file : str, optional
            The file path where the reversed video will be saved. If not provided, a default file name will be generated based on the original video file name.

        include_audio : bool, optional, default: True
            If True, the audio track is also reversed and included in the output. If False, only the video is reversed.

        force_replace : bool, optional, default: False
            If True, it will overwrite the output file if it already exists. If False and the file exists, the function may raise an error or generate a new file name.

        :param output_file:
        :type output_file:
        :param include_audio:
        :type include_audio:
        :param force_replace:
        :type force_replace:
        :return:
        :rtype:
        """
        if output_file is None:
            output_file = f"{self.file_name}_reverse{self.file_extension}"

        super().reverse_video(output_file=output_file, include_audio=include_audio, force_replace=force_replace)


    def scale(self,
              arg: str = None, *,
              width: int = None,
              height: int = None,
              factor: int = None,
              force_replace: bool = False,
              output_file: str = None):

        """
        Scales the video by either width and height or by a scaling factor.
        arg : str, optional
        A custom scaling argument (e.g., using FFmpeg scale syntax). If provided, it will override the width, height, and factor parameters.

        Parameters:
        ----------

        width : int, optional
            The desired width of the output video. If height is not provided, the aspect ratio is preserved.

        height : int, optional
            The desired height of the output video. If width is not provided, the aspect ratio is preserved.

        factor : int, optional
            A scaling factor by which to multiply the original width and height (e.g., factor=2 will double the resolution).

        force_replace : bool, optional, default: False
            If True, it will overwrite the output file if it already exists. If False and the file exists, the function may raise an error or generate a new file name.

        output_file : str, optional
            The file path where the scaled video will be saved. If not provided, a default file name will be generated based on the original video file name.

        :param arg:
        :type arg:
        :param width:
        :type width:
        :param height:
        :type height:
        :param factor:
        :type factor:
        :param force_replace:
        :type force_replace:
        :param output_file:
        :type output_file:
        :return:
        :rtype:
        """
        _filter = "scale="
        if arg:
            _w, _h = FFMpegHelper.dimension_arg_eval(arg)
            if _w and _h:
                width = _w
                height = _h

        if factor:
            width = f"{factor}*iw"
            height = f"{factor}*ih"

        _filter += f"{width}x{height}"

        if output_file is None:
            output_file = f"{self.file_name}_{width}{self.file_extension}"

        super().scale(filter_string=_filter, force_replace=force_replace, output_file=output_file)

    def convert_to_gif(self,
                       output_file: str = None,
                       seek: str = None,
                       end: str = None,
                       fps: int = None,
                       width: int = None,
                       force_replace: bool = False):
        """
        Converts a portion of the video to a GIF.
        Parameters:
        ----------
        output_file : str, optional
            The file path where the GIF will be saved. If not provided, a default file name will be generated based on
            the original video file name.

        seek : str, optional
            The timestamp in "HH:MM:SS" format from which to start the GIF. If not provided, the GIF starts from the
            beginning.

        end : str, optional
            The timestamp in "HH:MM:SS" format to stop the GIF. If not provided, the GIF will capture a default
            duration after the seek time.

        fps : int, optional
            The frames per second for the GIF. If not provided, a default FPS value is used.

        width : int, optional
            The width of the output GIF. If provided, the height will be scaled proportionally to maintain the aspect
            ratio.

        force_replace : bool, optional, default: False
            If True, it will overwrite the output file if it already exists. If False and the file exists, the function
             may raise an error or generate a new file name.

        :param output_file:
        :type output_file:
        :param seek:
        :type seek:
        :param end:
        :type end:
        :param fps:
        :type fps:
        :param width:
        :type width:
        :param force_replace:
        :type force_replace:
        :return:
        :rtype:
        """
        _file_extension = '.gif'
        video_duration = self.metadata.get('duration')

        kwargs = {
            'force_replace': force_replace or False,
            'output_file': output_file or f"{self.file_name}_image{_file_extension}",
        }

        _filter_args = {
            'fps': fps or 10,
            'scale': f'{width or 320}:-1:flags=lanczos'
        }
        _seek, _end = validate_time_range(video_duration, seek=seek, end=end, max_length=Config.gif_file_length)
        super().convert_to_gif(seek=_seek, end=_end, filter_string=_filter_args, **kwargs)

    def add_watermark(self,
                      watermark_file, *,
                      position=None,
                      padding=None,
                      scale_factor=None,
                      output_file=None,
                      force_replace=False,
                      transparency=None):
        """
        Adds a watermark to the video with options for position, scaling, transparency, and padding.

        Parameters:
        -----------
        watermark_file : str
            Path to the watermark image file (e.g., a PNG with transparency).

        position : tuple, optional
            Tuple specifying the x and y position of the watermark on the video (e.g., ('top-right', 'bottom-left')).
            If None, the default position is the top-left corner of the video.

        padding : int or tuple, optional
            Padding around the watermark. Can be a single integer for uniform padding or a tuple for (horizontal,
            vertical) padding.
            Default is None (no padding).

        scale_factor : float, optional
            Factor to scale the watermark relative to its original size. A value less than 1 will reduce the size, and
            greater than 1 will increase it.
            Default is None (original size is used).

        output_file : str, optional
            Path to the output video file. If None, a default output file will be generated based on the input filename.

        force_replace : bool, optional
            If True, overwrite the existing output file if it exists. If False, an error will be raised if the output
             file already exists.
            Default is False.

        transparency : float, optional
            The transparency level for the watermark (between 0 and 1). A value of 0 means fully transparent
            (invisible), and 1 means fully opaque.
            Default is None (no transparency adjustment is made).

        :param watermark_file:
        :type watermark_file:
        :param position:
        :type position:
        :param padding:
        :type padding:
        :param scale_factor:
        :type scale_factor:
        :param output_file:
        :type output_file:
        :param force_replace:
        :type force_replace:
        :param transparency:
        :type transparency:
        :return:
        :rtype:
        """

        # setting default args
        kwargs = {
            'position': position or 'top_left',
            'padding': padding or 30,
            'scale_factor': scale_factor or 0.2,
            'transparency': transparency or 0.3
        }
        if output_file is None:
            output_file = f"{self.file_name}_mixed_{self.file_extension}"

        super().add_watermark(watermark_file, output_file=output_file, force_replace=force_replace, **kwargs)

    def add_text(self,
                 text,
                 font_file=None,
                 font_color=None,
                 font_size=None,
                 position=None,
                 enable_box=None,
                 box_color=None,
                 border_width=None,
                 transparency=None,
                 padding=None,
                 force_replace=None,
                 repeat=None,
                 start_after=None,
                 duration=None):

        """
        Adds a text overlay to a media file (e.g., video or image) with customizable options for font, positioning,
        style, and timing.
        :param text:
        :type text:
        :param font_file:
        :type font_file:
        :param font_color:
        :type font_color:
        :param font_size:
        :type font_size:
        :param position:
        :type position:
        :param enable_box:
        :type enable_box:
        :param box_color:
        :type box_color:
        :param border_width:
        :type border_width:
        :param transparency:
        :type transparency:
        :param padding:
        :type padding:
        :param force_replace:
        :type force_replace:
        :param repeat:
        :type repeat:
        :param start_after:
        :type start_after:
        :param duration:
        :type duration:
        :return:
        :rtype:
        """

        if not position:
            position = 'top_right'

        if isinstance(position, str):
            padding = padding or 30

        elif isinstance(position, tuple):
            padding = None

        kwargs = {
            'font_file': font_file or 'roboto.ttf',
            'font_color': font_color or 'white',
            'font_size': font_size or 24,
            'enable_box': enable_box or True,
            'box_color': box_color or 'black',
            'transparency': transparency or 0.5,
            'border_width': border_width or 5,
            'start_after': start_after,
            'duration': duration,
            'repeat': repeat
        }

        super().add_text(text, position=position, padding=padding, force_replace=force_replace, **kwargs)
