"""init module for qr_colored"""

from qr_colored import _version
from qr_colored.app_logging import init_logging

init_logging()
VERSION = __version__ = _version.get_versions()['version']
