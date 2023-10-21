"""Region information."""
from __future__ import annotations

from boto3.session import Session


class _RegionInfo:
    """Region information."""

    def __init__(
        self: _RegionInfo, name: str, location: str, display_name: str
    ) -> None:
        """Initialize data.

        Args:
            name(str): Region name
            location(str): Region location
            display_name(str): Region display name
        """
        self.name = name
        self.location = location
        self.display_name = display_name


def get_regions(session: Session) -> list[_RegionInfo]:
    """."""
    ec2 = session.client("ec2")
    ssm = session.client("ssm")
    regions_res = ec2.describe_regions(
        Filters=[
            {
                "Name": "opt-in-status",
                "Values": ["opt-in-not-required", "opted-in"],
            }
        ]
    )
    region_names = [r["RegionName"] for r in regions_res["Regions"]]
    ret: list[_RegionInfo] = []
    for region_name in region_names:
        param_path = (
            "/aws/service/global-infrastructure/regions/" + region_name
        )
        params = ssm.get_parameters_by_path(Path=param_path)
        location: str | None = None
        display_name: str | None = None
        for param in params["Parameters"]:
            if param["Name"] == param_path + "/geolocationRegion":
                location = param["Value"]
            if param["Name"] == param_path + "/longName":
                display_name = param["Value"]
        if not location or not display_name:
            continue
        ret.append(_RegionInfo(region_name, location, display_name))
    return ret
