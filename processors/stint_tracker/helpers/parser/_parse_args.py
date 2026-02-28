import argparse
from ._make_parser import _make_parser

def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments and return the resulting namespace."""
    return _make_parser().parse_args()