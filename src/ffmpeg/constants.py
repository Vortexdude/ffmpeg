class Columns:
    CHAPTERS: str = '-show_chapters'
    STREAMS: str = '-show_streams'

class Filters:
    AUDIO_REVERSE: str = 'areverse'
    VIDEO_REVERSE: str = 'reverse'
    JSON: str = 'json'

class CODECS:
    COPY: str = 'copy'

class Flags:
    INPUT: str = "-i"
    AUDIO_CODEC: str = '-acodec'
    VIDEO_CODEC: str = '-vcodec'
    COMMON_CODEC: str = '-c'
    SEEK: str = '-ss'
    TO: str = '-to'
    VERBOSITY: str = '-v'
    AUDIO_QUALITY: str = '-q:a'
    VIDEO_QUALITY: str = '-q:v'
    MAP_STREAM: str = '-map'
    VIDEO_FRAME: str = '-frames:v'
    NO_AUDIO: str = '-an'
    COPY: str = 'copy'
    VIDEO_FILTER: str = '-vf'
    AUDIO_FILTER: str = '-af'
    FORMATTER: str = '-print_format'

class DefaultProperties:

    def __init__(self):
        self._audio_codec: list = []
        self._video_codec: list = []
        self._input: list = []
        self._seek: list = []
        self._to: list = []
        self._verbosity = []
        self._command_codec = []
        self._audio_quality = []
        self._video_quality = []
        self._map_stream = []
        self._video_frames = []
        self._options = []
        self._video_filter = []
        self._audio_filter = []

    @property
    def input(self):
        return self._input

    @property
    def audio_codec(self):
        return self._audio_codec

    @property
    def video_codec(self):
        return self._video_codec

    @property
    def to(self):
        return self._to

    @property
    def seek(self):
        return self._seek

    @property
    def common_codec(self):
        return self._command_codec

    @property
    def verbosity(self):
        return self._verbosity

    @property
    def audio_quality(self):
        return self._audio_quality

    @property
    def video_quality(self):
        return self._video_quality

    @property
    def map_stream(self):
        return self._map_stream

    @property
    def video_frames(self):
        return self._video_frames

    @property
    def options(self):
        return self._options

    @property
    def audio_filter(self):
        return self._audio_filter

    @property
    def video_filter(self):
        return self._video_filter

    @input.setter
    def input(self, value):
        if isinstance(value, str):
            self._input = [Flags.INPUT, value]
        elif isinstance(value, list):
            self._input = value
        else:
            raise ValueError("Value must be a string or a list of strings")

    @audio_codec.setter
    def audio_codec(self, value):
        self._audio_codec = [Flags.AUDIO_CODEC, value]

    @video_codec.setter
    def video_codec(self, value):
        self._video_codec = [Flags.VIDEO_CODEC, value]

    @to.setter
    def to(self, value):
        self._to = [Flags.TO, value]

    @seek.setter
    def seek(self, value):
        self._seek = [Flags.SEEK, value]

    @common_codec.setter
    def common_codec(self, value):
        self._command_codec = [Flags.COMMON_CODEC, value]

    @verbosity.setter
    def verbosity(self, value):
        self._verbosity = [Flags.VERBOSITY, value]

    @map_stream.setter
    def map_stream(self, value):
        self._map_stream = [Flags.MAP_STREAM, value]

    @audio_quality.setter
    def audio_quality(self, value):
        self._audio_quality = [Flags.AUDIO_QUALITY, value]

    @video_quality.setter
    def video_quality(self, value):
        self._video_quality = [Flags.VIDEO_QUALITY, value]

    @video_frames.setter
    def video_frames(self, value):
        self._video_frames = [Flags.VIDEO_FRAME, value]

    @options.setter
    def options(self, value):
        self._options = [value]

    @video_filter.setter
    def video_filter(self, value):
        self._video_filter = [Flags.VIDEO_FILTER, value]

    @audio_filter.setter
    def audio_filter(self, value):
        self._audio_filter = [Flags.AUDIO_FILTER, value]
