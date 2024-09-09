import logging


logger = logging.getLogger("ffmpeg")

logging.basicConfig(
    format="[{levelname}] - {asctime} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
    )
