"""
imfidata: A Python package for retrieving and working with IMF SDMX data.
"""

from importlib.metadata import version, PackageNotFoundError

# Public API
from .imfclient import IMFClient
from .utils import DimensionEnv, sanitize, make_key_str, convert_time_period_auto

__all__ = [
    "IMFClient",
    "DimensionEnv",
    "sanitize",
    "make_key_str",
    "convert_time_period_auto"
]

try:
    __version__ = version("imfidata")
except PackageNotFoundError:
    __version__ = "unknown"
