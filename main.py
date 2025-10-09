from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from functions.appFunctions import bootUp, getMountMethod, getAllUserDownloadsFresh, getMountRefreshTime
from functions.databaseFunctions import closeAllDatabases
from library.app import DEBUG_MODE
import logging
from sys import platform
import os

logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE == True else logging.INFO,
    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.getLogger("httpx").setLevel(logging.WARNING)

if __name__ == "__main__":
    bootUp()
    mount_method = getMountMethod()

    if mount_method == "strm":
        scheduler = BlockingScheduler()
    elif mount_method == "fuse":
        if platform == "win32":
            logging.error("The FUSE mount method is not supported on Windows. Please use the STRM mount method or run this application on a Linux system.")
            exit(1)
        scheduler = BackgroundScheduler()
    else:
        logging.error("Invalid mount method specified.")
        exit(1)

    user_downloads = getAllUserDownloadsFresh()

    scheduler.add_job(
        getAllUserDownloadsFresh,
        "interval",
        hours=getMountRefreshTime(),
        id="get_all_user_downloads_fresh",
    )

    try:
        logging.info("Starting scheduler and mounting...")
        if mount_method == "strm":
            from functions.stremFilesystemFunctions import runStrm
            runStrm()
            scheduler.add_job(
                runStrm,
                "interval",
                minutes=5,
                id="run_strm",
            )
            scheduler.start()
        elif mount_method == "fuse":
            from functions.fuseFilesystemFunctions import runFuse
            scheduler.start()
            runFuse()
    except (KeyboardInterrupt, SystemExit):
        if mount_method == "fuse":
            from functions.fuseFilesystemFunctions import unmountFuse
            unmountFuse()
        elif mount_method == "strm":
            from functions.stremFilesystemFunctions import unmountStrm
            unmountStrm()
        closeAllDatabases()
        exit(0)