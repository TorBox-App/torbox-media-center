import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

SCAN_METADATA = os.getenv("ENABLE_METADATA", "false").lower() == "true"

class MountRefreshTimes(Enum):
    # times are shown in hours
    slowest = 24 # 24 hours
    very_slow = 12 # 12 hours
    slow = 6 # 6 hours
    normal = 3 # 3 hours
    fast = 2 # 2 hours
    ultra_fast = 1 # 1 hour
    instant = 0.1 # 6 minutes

MOUNT_REFRESH_TIME = os.getenv("MOUNT_REFRESH_TIME", MountRefreshTimes.normal.name)
MOUNT_REFRESH_TIME = MOUNT_REFRESH_TIME.lower()
assert MOUNT_REFRESH_TIME in [e.name for e in MountRefreshTimes], f"Invalid mount refresh time: {MOUNT_REFRESH_TIME}. Valid options are: {[e.name for e in MountRefreshTimes]}"

if MOUNT_REFRESH_TIME == "instant":
    print("!!! Instant mount refresh time may cause rate limiting issues with the API. Use with caution. !!!")

if SCAN_METADATA:
    print("!!! Metadata scanning is enabled. This may slow down the processing of files. !!!")
if MOUNT_REFRESH_TIME == "instant" and SCAN_METADATA:
    print("!!! Using instant mount refresh time with metadata scanning may lead to excessive API calls. Falling back to 'fast' refresh time. !!!")
    MOUNT_REFRESH_TIME = MountRefreshTimes.fast.value
else:
    MOUNT_REFRESH_TIME = MountRefreshTimes[MOUNT_REFRESH_TIME].value