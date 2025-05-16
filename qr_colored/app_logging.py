"""Logging Management for the Application"""

import json
import logging
from copy import copy
from logging import Formatter
from qr_colored.settings import load_settings


settings = load_settings()


class Colors:
    """ansi color codes"""

    BLACK = '30'
    BLACK_LIGHT = '30;1'
    RED = '31'
    RED_LIGHT = '31;1'
    GREEN = '32'
    GREEN_LIGHT = '32;1'
    YELLOW = '33'
    YELLOW_LIGHT = '33;1'
    BLUE = '34'
    BLUE_LIGHT = '34;1'
    MAGENTA = '35'
    MAGENTA_LIGHT = '35;1'
    CYAN = '36'
    CYAN_LIGHT = '36;1'
    WHITE = '37'
    WHITE_LIGHT = '37;1'
    BLACK_ON_RED = '41'
    Reset = 0


DEFAULT_LOG_LEVEL = logging.DEBUG
PREFIX = '\033['
SUFFIX = '\033[0m'
MAPPING = {
    'DEBUG': Colors.GREEN_LIGHT,
    'INFO': Colors.CYAN_LIGHT,
    'WARNING': Colors.YELLOW_LIGHT,
    'ERROR': Colors.RED_LIGHT,
    'CRITICAL': Colors.BLACK_ON_RED,
    'filename': Colors.CYAN,
    'func_name': Colors.BLUE,
    'asctime': Colors.YELLOW,
    'message': Colors.MAGENTA,
}


def colorize(text: str, color_ansi: str = Colors.WHITE_LIGHT) -> str:
    """colorize text in specified color"""
    return f'{PREFIX}{color_ansi}m{text}{SUFFIX}'


STDOUT_LOG_FORMAT = (
    f"[{colorize('%(asctime)s', MAPPING.get('asctime', Colors.WHITE_LIGHT))}] "
    f"[{colorize('%(filename)s', MAPPING.get('filename', Colors.CYAN))}: "
    f"{colorize('%(funcName)s', MAPPING.get('func_name', Colors.BLUE))}] "
    f"%(levelname)s {colorize(':', Colors.WHITE_LIGHT)} %(message)s"
)
STREAM_LOG_FORMAT = "[%(asctime)s] [%(filename)s: %(funcName)s] %(levelname)s : %(message)s"


class ColoredFormatter(Formatter):
    """custom coloured formatter class"""

    def __init__(self, patern):
        Formatter.__init__(self, patern)

    def format(self, record):

        # make a copy (important)
        colored_record = copy(record)

        # level name
        levelname = colored_record.levelname
        color_pattern_levelname = MAPPING.get(levelname, Colors.WHITE)
        colored_levelname = colorize(levelname, color_pattern_levelname)
        colored_record.levelname = colored_levelname

        return Formatter.format(self, colored_record)


def init_logging(mode='w') -> None:
    """configure logging settings"""

    if mode not in {'a', 'w'}:
        raise ValueError("mode must be one of {'a', 'w'}")

    # formatters
    simple_formatter = logging.Formatter(STREAM_LOG_FORMAT)
    colored_formatter = ColoredFormatter(STDOUT_LOG_FORMAT)

    # stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(colored_formatter)
    stream_handler.setLevel = DEFAULT_LOG_LEVEL  # pyright: ignore

    # file handler
    file_handler = logging.FileHandler(
        filename=settings.log.filename,
        mode=mode,
        encoding='utf-8',
    )
    file_handler.setFormatter(simple_formatter)
    file_handler.setLevel = DEFAULT_LOG_LEVEL  # pyright: ignore

    # define basic configuration for logging
    logging.basicConfig(
        level=DEFAULT_LOG_LEVEL,
        handlers=[stream_handler, file_handler],
    )

    # ignore logging for these libraries
    logging.getLogger('boto3').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('s3fs').setLevel(logging.CRITICAL)
    logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('fsspec').setLevel(logging.CRITICAL)
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    logging.getLogger('aiobotocore').setLevel(logging.CRITICAL)
    logging.getLogger('azure').setLevel(logging.CRITICAL)


def beautify(dict_like_data: dict, indent: int = 4, sort_keys: bool = True) -> str:
    """beautify a dictionary with indentation"""
    return json.dumps(dict_like_data, indent=indent, sort_keys=sort_keys)
