"""Availability zones."""
from __future__ import annotations

from enum import Enum

from boto3.session import Session


class ZoneType(str, Enum):
    """Zone type."""

    AZ = "availability-zone"
    LOCAL = "local-zone"
    WAVELENGTH = "wavelength-zone"


class AvailabilityZone:
    """Availability zone."""

    def __init__(
        self: AvailabilityZone, name: str, zone_id: str, zone_type: ZoneType
    ) -> None:
        """Initialize data.

        Args:
            name(str): Zone name, such as us-west-2a
            zone_id(str): Zone ID, such as usw2-az1
            zone_type(ZoneType): Zone type
        """
        self.name = name
        self.zone_id = zone_id
        self.zone_type = zone_type


def get_zones(session: Session, region_name: str) -> list[AvailabilityZone]:
    """Get availability zones.

    Args:
        session(Session): Boto3 session
        region_name(str): Region name

    Returns:
        list: Availability zones
    """
    ec2 = session.client("ec2", region_name=region_name)
    azs_res = ec2.describe_availability_zones(
        Filters=[
            {
                "Name": "opt-in-status",
                "Values": ["opt-in-not-required", "opted-in"],
            }
        ]
    )
    return [
        AvailabilityZone(
            az["ZoneName"], az["ZoneId"], ZoneType(az["ZoneType"])
        )
        for az in azs_res["AvailabilityZones"]
    ]
