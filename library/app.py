import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class MountRefreshTimes(Enum):
    # times are shown in hours
    slow = 3 # 3 hours
    normal = 2 # 2 hours
    fast = 1 # 1 hour
    instant = 0.10 # 6 minutes

MOUNT_REFRESH_TIME = os.getenv("MOUNT_REFRESH_TIME", MountRefreshTimes.fast.name)
MOUNT_REFRESH_TIME = MOUNT_REFRESH_TIME.lower()
assert MOUNT_REFRESH_TIME in [e.name for e in MountRefreshTimes], f"Invalid mount refresh time: {MOUNT_REFRESH_TIME}. Valid options are: {[e.name for e in MountRefreshTimes]}"

MOUNT_REFRESH_TIME = MountRefreshTimes[MOUNT_REFRESH_TIME].value

DEBUG_MODE = os.getenv("DEBUG_MODE", False) in [True,'true']
