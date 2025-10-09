import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class MountRefreshTimes(Enum):
    # times are shown in hours
    slowest = 24 # 24 hours
    very_slow = 12 # 12 hours
    slow = 6 # 6 hours
    normal = 3 # 3 hours
    fast = 2 # 2 hours
    instant = 1 # 1 hour

MOUNT_REFRESH_TIME = os.getenv("MOUNT_REFRESH_TIME", MountRefreshTimes.normal.name)
MOUNT_REFRESH_TIME = MOUNT_REFRESH_TIME.lower()
assert MOUNT_REFRESH_TIME in [e.name for e in MountRefreshTimes], f"Invalid mount refresh time: {MOUNT_REFRESH_TIME}. Valid options are: {[e.name for e in MountRefreshTimes]}"

MOUNT_REFRESH_TIME = MountRefreshTimes[MOUNT_REFRESH_TIME].value