import logging
from os.path import exists, getsize

from mpl_theme_tweaker.utils import logPath


def setup_logger():
    logger = logging.getLogger("mpl_theme_tweaker")
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger

    # setup console logger
    console_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(filename)s:%(lineno)d\n\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # setup file logger
    logfile = logPath() / "mpl_theme_tweaker.log"
    MAX_LOG_FILE_SIZE = 20  # config.log.max_file_size_mb
    mode = "a" if exists(logfile) and (getsize(logfile) >= MAX_LOG_FILE_SIZE) else "w"
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d\n\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = logging.FileHandler(logfile, mode, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger


log = setup_logger()
