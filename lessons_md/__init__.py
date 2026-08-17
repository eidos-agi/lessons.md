"""lessons.md — the learning forge. Durable lessons from execution."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lessons-md")
except PackageNotFoundError:  # running from source without an install
    __version__ = "0.0.0+unknown"
