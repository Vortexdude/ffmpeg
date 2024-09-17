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
