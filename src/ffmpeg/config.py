from .logging import GuardianLogger


class Config:
    output_dir: str = "outputs"
    supported_filters: list = ['reverse']
    log_level: str = 'info'

    @classmethod
    def set_log_level(cls, value):
        cls.log_level = value


setting = Config()

log_init = GuardianLogger('info', "FFMPEG")
logger = log_init.get_logger()
logger.debug("Logging Initialize ... .. .")
