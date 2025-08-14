"""
imfidata: A Python package for retrieving and working with IMF SDMX data.
"""

from importlib.metadata import version, PackageNotFoundError

# Public API
from . import auth
from . import metadata
from . import retrieval
from .utils import DimensionEnv, sanitize, make_key_str

__all__ = [
    "auth",
    "metadata",
    "retrieval",
    "DimensionEnv",
    "sanitize",
    "make_key_str",
    "sdmx_client"
]

try:
    __version__ = version("imfidata")
except PackageNotFoundError:
    __version__ = "unknown"
