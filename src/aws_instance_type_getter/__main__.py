"""Main program."""
from __future__ import annotations

from boto3.session import Session
from openpyxl import Workbook

from .args import parse_command_args
from .availability_zone import get_zones
from .instance_type import get_instance_types
from .region import get_regions

args = parse_command_args()
if args.profile:
    session = Session(profile_name=args.profile)
else:
    session = Session()

workbook = Workbook()

regions = get_regions(session)
for region in regions:
    zones = get_zones(session, region.name)
    instance_types = get_instance_types(session, region.name)
