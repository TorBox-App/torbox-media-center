from library.app import RAW_MODE
from functions.torboxFunctions import getUserDownloads, DownloadType
from library.filesystem import MOUNT_METHOD, MOUNT_PATH
from library.app import MOUNT_REFRESH_TIME
from library.torbox import TORBOX_API_KEY
from functions.databaseFunctions import getAllData, clearDatabase
import logging
import os
import shutil

def initializeFolders():
    folders = [MOUNT_PATH]
    if not RAW_MODE:
        folders.extend([
            os.path.join(MOUNT_PATH, "movies"),
            os.path.join(MOUNT_PATH, "series"),
        ])
    for folder in folders:
        if os.path.exists(folder):
            logging.debug(f"Folder {folder} already exists. Deleting...")
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        else:
            logging.debug(f"Creating folder {folder}...")
            os.makedirs(folder, exist_ok=True)

def getAllUserDownloadsFresh():
    all_downloads = []
    logging.info("Fetching all user downloads...")
    for download_type in DownloadType:
        logging.debug(f"Clearing database for {download_type.value}...")
        success, detail = clearDatabase(download_type.value)
        if not success:
            logging.error(f"Error clearing {download_type.value} database: {detail}")
            continue
        logging.debug(f"Fetching {download_type.value} downloads...")
        downloads, success, detail = getUserDownloads(download_type)
        if not success:
            logging.error(f"Error fetching {download_type.value}: {detail}")
            continue
        if not downloads:
            logging.info(f"No {download_type.value} downloads found.")
            continue
        all_downloads.extend(downloads)
        logging.debug(f"Fetched {len(downloads)} {download_type.value} downloads.")
    return all_downloads

def getAllUserDownloads():
    all_downloads = []
    for download_type in DownloadType:
        logging.debug(f"Fetching {download_type.value} downloads...")
        downloads, success, detail = getAllData(download_type.value)
        if not success:
            logging.error(f"Error fetching {download_type.value}: {detail}")
            continue
        all_downloads.extend(downloads)
        logging.debug(f"Fetched {len(downloads)} {download_type.value} downloads.")
    return all_downloads

def bootUp():
    logging.debug("Booting up...")
    logging.info("Mount method: %s", MOUNT_METHOD)
    logging.info("Mount path: %s", MOUNT_PATH)
    logging.info("TorBox API Key: %s", TORBOX_API_KEY)
    logging.info("Mount refresh time: %s %s", MOUNT_REFRESH_TIME, "hours")
    initializeFolders()

    return True

def getMountMethod():
    return MOUNT_METHOD

def getMountPath():
    return MOUNT_PATH

def getMountRefreshTime():
    return MOUNT_REFRESH_TIME
