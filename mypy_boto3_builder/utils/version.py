"""
Version-related utils.
"""

import contextlib

import pkg_resources
from boto3 import __version__ as boto3_version
from botocore import __version__ as botocore_version
from newversion import Version

from mypy_boto3_builder.constants import PACKAGE_NAME


def get_builder_version() -> str:
    """
    Get program version.
    """
    with contextlib.suppress(pkg_resources.DistributionNotFound):
        return pkg_resources.get_distribution(PACKAGE_NAME).version

    return "0.0.0"


def get_min_build_version(version: str) -> str:
    """
    Get min version build version by setting micro to 0.
    """
    return Version(version).replace(micro=0).get_stable().dumps()


def get_max_build_version(version: str) -> str:
    """
    Get min version build version by bumping minor.
    """
    return Version(version).bump_minor().get_stable().dumps()


def get_botocore_version() -> str:
    """
    Get botocore package version.
    """
    return botocore_version


def get_boto3_version() -> str:
    """
    Get boto3 package version.
    """
    return boto3_version


def get_aiobotocore_version() -> str:
    """
    Get aiobotocore package version.
    """
    try:
        from aiobotocore import __version__ as version
    except ImportError:
        raise RuntimeError("aiobotocore is not installed")
    return version


def get_aioboto3_version() -> str:
    """
    Get aioboto3 package version.
    """
    try:
        from aioboto3 import __version__ as version  # type: ignore
    except ImportError:
        raise RuntimeError("aioboto3 is not installed")

    return version
