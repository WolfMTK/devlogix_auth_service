import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_logging(path: Path):
    log_dir = path
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'bot.log'
    rotating_file_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5,
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_file_handler, logging.StreamHandler()),
    )
