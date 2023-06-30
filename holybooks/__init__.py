from .client import *
from .http import *
from .quran import *
from .bible import *
from .errors import *
from .mixins import *
from .translation import *
from typing import NamedTuple, Literal


__title__ = "holybooks"
__version__ = "1.0.0a1"
__author__ = "TheGenocides"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present TheGenocides"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=1, minor=0, micro=0, releaselevel="alpha", serial=1)

assert version_info.releaselevel in (
    "alpha",
    "beta",
    "candidate",
    "final",
), "Invalid release level given."