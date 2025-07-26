import os
from library.filesystem import MOUNT_PATH
import logging
from functions.appFunctions import getAllUserDownloads
import shutil

def generateFolderPath(data: dict):
    """
    Takes in a user download and returns the folder path for the download.

    Series (Year)/Season XX/Title SXXEXX.ext
    Movie (Year)/Title (Year).ext

    """
    root_folder = data.get("metadata_rootfoldername", None)
    metadata_foldername = data.get("metadata_foldername", None)

    if not root_folder and not metadata_foldername:
        return None

    if data.get("metadata_mediatype") == "series":
        folder_path = os.path.join(
            root_folder,
            metadata_foldername,
        )
    elif data.get("metadata_mediatype") == "movie":
        folder_path = os.path.join(
            root_folder
        )

    elif data.get("metadata_mediatype") == "anime":
        folder_path = os.path.join(
            root_folder,
            metadata_foldername,
        )
    else:
        folder_path = os.path.join(
            root_folder
        )
    return folder_path

def generateStremFile(file_path: str, url: str, type: str, file_name: str):
    if file_path is None:
        return
    if type == "movie":
        type = "movies"
    elif type == "series":
        type = "series"
    elif type == "anime":
        type = "series"

    full_path = os.path.join(MOUNT_PATH, type, file_path)

    try:
        os.makedirs(full_path, exist_ok=True)
        with open(f"{full_path}/{file_name}.strm", "w") as file:
            file.write(url)
        logging.debug(f"Created strm file: {full_path}/{file_name}.strm")
        return True
    except OSError as e:
        logging.error(f"Error creating strm file (likely bad or missing permissions): {e}")
        return False
    except FileNotFoundError as e:
        logging.error(f"Error creating strm file (likely bad naming scheme of file): {e}")
        return False
    except Exception as e:
        logging.error(f"Error creating strm file: {e}")
        return False

def runStrm():
    all_downloads = getAllUserDownloads()
    for download in all_downloads:
        file_path = generateFolderPath(download)
        if file_path is None:
            continue
        generateStremFile(file_path, download.get("download_link"), download.get("metadata_mediatype"), download.get("metadata_filename"))

    logging.debug(f"Updated {len(all_downloads)} strm files.")

def unmountStrm():
    """
    Deletes all strm files and any subfolders in the mount path for cleaning up.
    """
    folders = [
        MOUNT_PATH,
        os.path.join(MOUNT_PATH, "movies"),
        os.path.join(MOUNT_PATH, "series"),
    ]
    for folder in folders:
        if os.path.exists(folder):
            logging.debug(f"Folder {folder} already exists. Deleting...")
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)