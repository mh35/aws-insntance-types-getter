"""Argument parser."""
from __future__ import __annotations__

from argparse import ArgumentParser


class _CommandArgument:
    """Command arguments."""

    def __init__(self, profile: str | None, output: str) -> None:
        """Initialize data.

        Args:
            profile(str): AWS profile name
            output(str): Output filename
        """
        self.profile = profile
        self.output = output


def parse_command_args() -> _CommandArgument:
    """Parse command args.

    Returns:
        _CommandArgument: Command arguments data class object
    """
    parser = ArgumentParser(description="EC2 instance types info getter")
    parser.add_argument("-p", "--profile", help="AWS profile name")
    parser.add_argument(
        "-o", "--output", help="Output filename", default="out.xlsx"
    )
    args = parser.parse_args()
    profile: str | None = args.profile
    output: str = args.output
    return _CommandArgument(profile, output)
