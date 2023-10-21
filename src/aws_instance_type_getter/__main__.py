"""Main program."""
from __future__ import annotations

from boto3.session import Session

from .args import parse_command_args
from .region import get_regions

args = parse_command_args()
if args.profile:
    session = Session(profile_name=args.profile)
else:
    session = Session()

regions = get_regions(session)
