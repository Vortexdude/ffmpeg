import logging

class Guardian(logging.Formatter):
    GREEN = "\x1b[32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    GRAY = "\x1b[38;20m"
    LIGHT_GRAY = "\033[0;37m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    WHITE = "\x1b[0m"
    RESET = "\x1b[0m"

    custom_formatter = "[%(asctime)s][%(levelname)s] - %(message)s - %(filename)8s:%(lineno)s -%(funcName)10s()"

    FORMAT = {
        logging.DEBUG: GRAY + custom_formatter + RESET,
        logging.INFO: CYAN + custom_formatter + RESET,
        logging.WARNING: YELLOW + custom_formatter + RESET,
        logging.ERROR: RED + custom_formatter + RESET,
        logging.CRITICAL: BOLD_RED + custom_formatter + RESET
    }

    def format(self, record):
        log_fmt = self.FORMAT.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class GuardianLogger:
    def __init__(self, log_level, logger_namespace):
        if log_level is None:
            raise Exception("Please Specify the loglevel")

        log_levels = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warning': logging.WARN,
            'warn': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }
        logger = logging.getLogger(__name__)

        logger.setLevel(log_levels[log_level])
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Guardian())
        logger.addHandler(console_handler)
        self.logger = logging.LoggerAdapter(
            logger,
            {"logger_namespace": logger_namespace}
        )
        self.log_level = self.logger.logger.level

    def get_logger(self):
        return self.logger
