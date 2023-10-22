"""Instance type module."""
from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING

from boto3.session import Session

if TYPE_CHECKING:
    from mypy_boto3_ec2.type_defs import InstanceTypeInfoTypeDef


class CpuArchitectures(str, Enum):
    """CPU architectures."""

    ARM64 = "arm64"
    ARM64_MAC = "arm64_mac"
    X86 = "i386"
    X64 = "x86_64"
    X64_MAC = "x86_64_mac"


class NvmeSupportStatus(str, Enum):
    """NVMe support status."""

    REQUIRED = "required"
    SUPPORTED = "supported"
    NOT_SUPPORTED = "unsupported"


class InstanceStorageType(str, Enum):
    """Instance storage type."""

    SSD = "ssd"
    HDD = "hdd"


class EbsOptimizeSupportStatus(str, Enum):
    """EBS optimize support status."""

    DEFAULT_ENABLED = "default"
    CAN_ENABLE = "supported"
    NOT_SUPPORTED = "unsupported"


class _InstanceStorageInfo:
    """Instance storage information."""

    def __init__(
        self: _InstanceStorageInfo,
        size: int,
        count: int,
        storage_type: InstanceStorageType,
    ) -> None:
        """Initialize data.

        Args:
            size(int): Size in GB
            count(int): The number of instance store disks
            storage_type(InstanceStorageType): Instance store type
        """
        self.size = size
        self.count = count
        self.storage_type = storage_type


class InstanceNetworkPerformanceType(str, Enum):
    """Network performance type."""

    UPBOUND = "UPBOUND"
    SINGLE = "SINGLE"
    MULTIPLE = "MULTIPLE"
    FUZZY = "FUZZY"
    UNKNOWN = "UNKNOWN"


class InstanceNetworkFuzzySpeed(str, Enum):
    """Network performance fuzzy speed."""

    VERY_LOW = "Very Low"
    LOW = "Low"
    LOW_TO_MODERATE = "Low to Moderate"
    MODERATE = "Moderate"
    HIGH = "High"
    INVALID = "Invalid"


class _InstanceNetworkPerformance:
    """Instance network performance."""

    def __init__(self: _InstanceNetworkPerformance, spec: str) -> None:
        """Parse and initialize.

        Args:
            spec(str): Speed spec
        """
        self._spec = spec
        if spec == "Very Low":
            self._performance_type = InstanceNetworkPerformanceType.FUZZY
            self._performance_fuzzy_value = InstanceNetworkFuzzySpeed.VERY_LOW
            self._speed = 0.0
            self._aggregation = 1
        elif spec == "Low":
            self._performance_type = InstanceNetworkPerformanceType.FUZZY
            self._performance_fuzzy_value = InstanceNetworkFuzzySpeed.LOW
            self._speed = 0.0
            self._aggregation = 1
        elif spec == "Low to Moderate":
            self._performance_type = InstanceNetworkPerformanceType.FUZZY
            self._performance_fuzzy_value = (
                InstanceNetworkFuzzySpeed.LOW_TO_MODERATE
            )
            self._speed = 0.0
            self._aggregation = 1
        elif spec == "Moderate":
            self._performance_type = InstanceNetworkPerformanceType.FUZZY
            self._performance_fuzzy_value = InstanceNetworkFuzzySpeed.MODERATE
            self._speed = 0.0
            self._aggregation = 1
        elif spec == "High":
            self._performance_type = InstanceNetworkPerformanceType.FUZZY
            self._performance_fuzzy_value = InstanceNetworkFuzzySpeed.HIGH
            self._speed = 0.0
            self._aggregation = 1
        else:
            self._performance_fuzzy_value = InstanceNetworkFuzzySpeed.INVALID
            up_to_md = re.match(r"^Up to (\d+(\.\d+)?) Gigabit", spec)
            if up_to_md:
                self._performance_type = InstanceNetworkPerformanceType.UPBOUND
                self._speed = float(up_to_md[1])
                self._aggregation = 1
            else:
                rest_md = re.match(r"((\d+)x )?(\d+(\.\d+)?) Gigabit", spec)
                if rest_md:
                    self._speed = float(rest_md[3])
                    if rest_md[2]:
                        self._performance_type = (
                            InstanceNetworkPerformanceType.MULTIPLE
                        )
                        self._aggregation = int(rest_md[2])
                    else:
                        self._performance_type = (
                            InstanceNetworkPerformanceType.SINGLE
                        )
                        self._aggregation = 1
                else:
                    self._performance_type = (
                        InstanceNetworkPerformanceType.UNKNOWN
                    )
                    self._speed = 0.0
                    self._aggregation = 1

    @property
    def performance_type(
        self: _InstanceNetworkPerformance,
    ) -> InstanceNetworkPerformanceType:
        """Performance type.

        Returns:
            InstanceNetworkPerformanceType: Performance type
        """
        return self._performance_type

    @property
    def performance_fuzzy_value(
        self: _InstanceNetworkPerformance,
    ) -> InstanceNetworkFuzzySpeed:
        """Performance fuzzy speed.

        Returns:
            InstanceNetworkFuzzySpeed: Fuzzy speed value

        Raises:
            ValueError: If this object is not FUZZY speed type
        """
        if self.performance_type != InstanceNetworkPerformanceType.FUZZY:
            raise ValueError("Speed is not fuzzy")
        return self._performance_fuzzy_value

    @property
    def speed(self: _InstanceNetworkPerformance) -> float:
        """Performance speed.

        Returns:
            float: Speed value in Gbps

        Raises:
            ValueError: If this object is FUZZY speed type
        """
        if self.performance_type == InstanceNetworkPerformanceType.FUZZY:
            raise ValueError("Speed is fuzzy")
        return self._speed

    @property
    def aggregation(self: _InstanceNetworkPerformance) -> int:
        """Aggregation number.

        Returns:
            int: Aggregation number. If not available, returns 1
        """
        return self._aggregation

    def __str__(self: _InstanceNetworkPerformance) -> str:
        """Get string format.

        Returns:
            str: Input spec value
        """
        return self._spec


class _NetworkCard:
    """Network card."""

    def __init__(
        self: _NetworkCard,
        index: int,
        performance: _InstanceNetworkPerformance,
        max_interfaces: int,
    ) -> None:
        """."""
        self.index = index
        self.performance = performance
        self.max_interfaces = max_interfaces


class EnaSupport(str, Enum):
    """ENA support status."""

    REQUIRED = "required"
    SUPPORTED = "supported"
    NOT_SUPPORTED = "unsupported"


class _GraphicBoard:
    """Graphic board."""

    def __init__(
        self: _GraphicBoard,
        name: str,
        manufacturer: str,
        count: int,
        memory: int,
    ) -> None:
        """."""
        self.name = name
        self.manufacturer = manufacturer
        self.count = count
        self.memory = memory


class _FpgaBoard:
    """FPGA board."""

    def __init__(
        self: _FpgaBoard,
        name: str,
        manufacturer: str,
        count: int,
        memory: int,
    ) -> None:
        """."""
        self.name = name
        self.manufacturer = manufacturer
        self.count = count
        self.memory = memory


class _InterfaceAccelerator:
    """Interface accelarator."""

    def __init__(
        self: _InterfaceAccelerator, name: str, manufacturer: str, count: int
    ) -> None:
        """."""
        self.name = name
        self.manufacturer = manufacturer
        self.count = count


class PlacementStrategy(str, Enum):
    """Placement strategy."""

    CLUSTER = "cluster"
    PARTITION = "partition"
    SPREAD = "spread"


class InstanceType:
    """Instance type data."""

    def __init__(self: InstanceType, data: "InstanceTypeInfoTypeDef") -> None:
        """."""
        self.name = data.get("InstanceType", "t1.micro")
        self.is_current = data.get("CurrentGeneration", True)
        usage_classes = data.get("SupportedUsageClasses", [])
        self.supports_on_demand = "on-demand" in usage_classes
        self.supports_spot = "spot" in usage_classes
        root_devices = data.get("SupportedRootDeviceTypes", [])
        self.supports_ebs_root = "ebs" in root_devices
        self.supports_instance_store_root = "instance-store" in root_devices
        self.support_cpus = [
            CpuArchitectures(arch)
            for arch in data.get("ProcessorInfo", {}).get(
                "SupportedArchitectures", []
            )
        ]
        self.cpu_speed = data.get("ProcessorInfo", {}).get(
            "SustainedClockSpeedInGhz", 0.0
        )
        self.supports_sev_snp = "amd-sev-snp" in data.get(
            "ProcessorInfo", {}
        ).get("SupportedFeatures", [])
        self.default_vcpus = data.get("VCpuInfo", {}).get("DefaultVCpus", 1)
        self.default_cores = data.get("VCpuInfo", {}).get("DefaultCores", 1)
        self.default_threads_per_core = data.get("VCpuInfo", {}).get(
            "DefaultThreadsPerCore", 1
        )
        self.memory_size = data.get("MemoryInfo", {}).get("SizeInMiB", 0)
        self.has_instance_store = data.get("InstanceStorageSupported", False)
        if self.has_instance_store:
            instance_store_info = data.get("InstanceStorageInfo", {})
            self.total_instance_store_size = instance_store_info.get(
                "TotalSizeInGB", 0
            )
            self.instance_store_disks = [
                _InstanceStorageInfo(
                    d.get("SizeInGB", 0),
                    d.get("Count", 1),
                    InstanceStorageType(d.get("Type", "ssd")),
                )
                for d in instance_store_info.get("Disks", [])
            ]
            self.instance_store_encryption = (
                instance_store_info.get("EncryptionSupport") == "required"
            )
        else:
            self.total_instance_store_size = 0
            self.instance_store_disks = []
            self.instance_store_nvme_support = NvmeSupportStatus.NOT_SUPPORTED
            self.instance_store_encryption = False
        ebs_status = data.get("EbsInfo", {})
        self.support_ebs_optimize = EbsOptimizeSupportStatus(
            ebs_status.get("EbsOptimizedSupport", "unsupported")
        )
        self.support_ebs_encrypt = (
            ebs_status.get("EncryptionSupport", "unsupported") == "supported"
        )
        self.support_ebs_nvme = (
            ebs_status.get("NvmeSupport", "supported") == "supported"
        )
        if self.support_ebs_optimize != EbsOptimizeSupportStatus.NOT_SUPPORTED:
            opt_info = ebs_status.get("EbsOptimizedInfo", {})
            self.ebs_optimize_base_band = opt_info.get(
                "BaselineBandwidthInMbps", 0
            )
            self.ebs_optimize_base_throughput = opt_info.get(
                "BaselineThroughputInMBps", 0.0
            )
            self.ebs_optimize_base_iops = opt_info.get("BaselineIops", 0)
            self.ebs_optimize_max_band = opt_info.get(
                "MaximumBandwidthInMbps", 0
            )
            self.ebs_optimize_max_throughput = opt_info.get(
                "MaximumThroughputInMBps", 0.0
            )
            self.ebs_optimize_max_iops = opt_info.get("MaximumIops", 0)
        else:
            self.ebs_optimize_base_band = 0
            self.ebs_optimize_base_throughput = 0.0
            self.ebs_optimize_base_iops = 0
            self.ebs_optimize_max_band = 0
            self.ebs_optimize_max_throughput = 0.0
            self.ebs_optimize_max_iops = 0
        net_info = data.get("NetworkInfo", {})
        net_perf_v = net_info.get("NetworkPerformance")
        if net_perf_v:
            self.net_performance: _InstanceNetworkPerformance | None = (
                _InstanceNetworkPerformance(net_perf_v)
            )
        else:
            self.net_performance = None
        self.max_net_interface = net_info.get("MaximumNetworkInterfaces", 1)
        self.max_net_cards = net_info.get("MaximumNetworkCards", 1)
        self.default_card_index = net_info.get("DefaultNetworkCardIndex", 0)
        self.net_cards = [
            _NetworkCard(
                c.get("NetworkCardIndex", i),
                _InstanceNetworkPerformance(c.get("NetworkPerformance", "")),
                c.get("MaximumNetworkInterfaces", 1),
            )
            for i, c in enumerate(net_info.get("NetworkCards", []))
        ]
        self.support_ipv6 = net_info.get("Ipv6Supported", False)
        self.ipv4_addr_per_interface = net_info.get(
            "Ipv4AddressesPerInterface", 1
        )
        self.ipv6_addr_per_interface = net_info.get(
            "Ipv6AddressesPerInterface", 1 if self.support_ipv6 else 0
        )
        self.ena_support = EnaSupport(
            net_info.get("EnaSupport", "unsupported")
        )
        self.efa_supported = net_info.get("EfaSupported", False)
        self.max_efa_interfaces = net_info.get("EfaInfo", {}).get(
            "MaximumEfaInterfaces", 1 if self.efa_supported else 0
        )
        if "GpuInfo" in data:
            self.gpu_support = True
            self.gpus = [
                _GraphicBoard(
                    g.get("Name", ""),
                    g.get("Manufacturer", ""),
                    g.get("Count", 1),
                    g.get("MemoryInfo", {}).get("SizeInMiB", 0),
                )
                for g in data.get("GpuInfo", {}).get("Gpus", [])
            ]
            self.total_gpu_memory = data.get("GpuInfo", {}).get(
                "TotalGpuMemoryInMiB", 0
            )
        else:
            self.gpu_support = False
            self.gpus = []
            self.total_gpu_memory = 0
        if "FpgaInfo" in data:
            self.fpga_support = True
            self.fpgas = [
                _FpgaBoard(
                    b.get("Name", ""),
                    b.get("Manufacturer", ""),
                    b.get("Count", 1),
                    b.get("MemoryInfo", {}).get("SizeInMiB", 0),
                )
                for b in data.get("FpgaInfo", {}).get("Fpgas", [])
            ]
            self.total_fpga_memory = data.get("FpgaInfo", {}).get(
                "TotalFpgaMemoryInMiB", 0
            )
        else:
            self.fpga_support = False
            self.fpgas = []
            self.total_fpga_memory = 0
        if "InferenceAcceleratorInfo" in data:
            self.interface_accelerator_support = True
            self.interface_accelerators = [
                _InterfaceAccelerator(
                    ia.get("Name", ""),
                    ia.get("Manufacturer", ""),
                    ia.get("Count", 1),
                )
                for ia in data.get("InferenceAcceleratorInfo", {}).get(
                    "Accelerators", []
                )
            ]
        else:
            self.interface_accelerator_support = False
        self.placement_strategies = [
            PlacementStrategy(pn)
            for pn in data.get("PlacementGroupInfo", {}).get(
                "SupportedStrategies", []
            )
        ]
        self.support_hibernation = data.get("HibernationSupported", False)
        self.burstable = data.get("BurstablePerformanceSupported", False)


def get_instance_types(
    session: Session, region_name: str
) -> list[InstanceType]:
    """."""
    ec2 = session.client("ec2", region_name=region_name)
    res = ec2.describe_instance_types()
    ret = [InstanceType(t) for t in res["InstanceTypes"]]
    while "NextToken" in res:
        res = ec2.describe_instance_types(NextToken=res["NextToken"])
        ret.extend([InstanceType(t) for t in res["InstanceTypes"]])
    return ret
