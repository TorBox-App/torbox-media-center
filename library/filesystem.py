import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class MountMethods(Enum):
    strm = "strm"
    fuse = "fuse"

MOUNT_METHOD = os.getenv("MOUNT_METHOD", MountMethods.strm.value)
assert MOUNT_METHOD in [method.value for method in MountMethods], "MOUNT_METHOD is not set correctly in .env file"

MOUNT_PATH = os.getenv("MOUNT_PATH", "./torbox")
assert MOUNT_PATH, "MOUNT_PATH is not set in .env file"

MIN_MEDIA_SIZE_MB = int(os.getenv("MIN_MEDIA_SIZE_MB", "30"))