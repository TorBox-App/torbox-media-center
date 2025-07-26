import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class MountMethods(Enum):
    strm = "strm"
    fuse = "fuse"

class SymlinkCreation(Enum):
    once = "once"
    spawn = "spawn"
    always = "always"

MOUNT_METHOD = os.getenv("MOUNT_METHOD", MountMethods.strm.value)
assert MOUNT_METHOD in [method.value for method in MountMethods], "MOUNT_METHOD is not set correctly in .env file"

MOUNT_PATH = os.getenv("MOUNT_PATH", "./torbox")
assert MOUNT_PATH, "MOUNT_PATH is not set in .env file"

SYMLINK_PATH = os.getenv("SYMLINK_PATH", None)

SYMLINK_CREATION = os.getenv("SYMLINK_CREATION", "always")
assert SYMLINK_CREATION in [symlink.value for symlink in SymlinkCreation], "SYMLINK_CREATION is not set correctly in .env file"
