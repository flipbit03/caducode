"""CaduCode - Minimalist coding agent with a single run_python tool."""

from importlib.metadata import version

__version__ = version("caducode")

from .cli import cli

__all__ = ["__version__", "cli"]
