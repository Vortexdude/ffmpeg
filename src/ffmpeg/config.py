import logging

class Config:
    output_dir: str = "outputs"
    supported_filters: list = ['reverse']
    log_level: str = 'info'


logger_mapping = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "fatal": logging.FATAL
}

logger = logging.getLogger("ffmpeg")

logging.basicConfig(
    format="[{levelname}] - {asctime} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logger_mapping[Config.log_level]
    )
