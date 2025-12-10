from library.app import RAW_MODE
import os
from library.filesystem import MOUNT_PATH
import stat
import errno
from functions.torboxFunctions import getDownloadLink, downloadFile
import time
import sys
import logging
from functions.appFunctions import getAllUserDownloads
import threading
from sys import platform

# Pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts # type: ignore # noqa: F401
except ImportError:
    pass
import fuse
from fuse import Fuse
if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-python doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)

LINK_AGE = 3 * 60 * 60 # 3 hours

class VirtualFileSystem:
    def __init__(self, files_list):
        self.files = files_list
        self.structure = self._build_structure()
        self.file_map = self._build_file_map()

    def _build_structure(self):
        if RAW_MODE:
            structure = { '/': set() }
            for f in self.files:
                original_path = f.get("path")
                if original_path:
                    # Split the path into parts
                    parts = original_path.split('/')
                    current_path = '/'
                    for part in parts[:-1]:  # Skip the filename
                        if part not in structure.get(current_path, set()):
                            structure.setdefault(current_path, set()).add(part)
                            current_path = f"{current_path}{part}/"
                            structure.setdefault(current_path, set())
            # Ensure consistent ordering
            for key in structure:
                structure[key] = sorted([item for item in structure[key] if item is not None])
            return structure
        else:
            structure = {
                '/': ['movies', 'series'],
                '/movies': set(),
                '/series': set()
            }
        
        
        for f in self.files:
            media_type = f.get('metadata_mediatype')
            root_folder = f.get('metadata_rootfoldername')
            
            if media_type == 'movie':
                path = f'/movies/{root_folder}'
                structure['/movies'].add(root_folder)
                
                if path not in structure:
                    structure[path] = set()
                structure[path].add(f.get('metadata_filename'))
                
            elif media_type == 'series':
                path = f'/series/{root_folder}'
                structure['/series'].add(root_folder)
                
                if path not in structure:
                    structure[path] = set()
                structure[path].add(f.get('metadata_foldername'))
                
                season_path = f'{path}/{f.get("metadata_foldername")}'
                if season_path not in structure:
                    structure[season_path] = set()
                structure[season_path].add(f.get('metadata_filename'))
        
        # consistent ordering
        for key in structure:
            structure[key] = sorted([item for item in structure[key] if item is not None])
            
        return structure

def _build_file_map(self):
    file_map = {}
    for f in self.files:
        if RAW_MODE:
            original_path = f.get("path")
            if original_path:
                path = f'/{original_path}'
                file_map[path] = f
        else:
            if f.get('metadata_mediatype') == 'movie':
                path = f'/movies/{f.get("metadata_rootfoldername")}/{f.get("metadata_filename")}'
                file_map[path] = f
            else:  # series
                path = f'/series/{f.get("metadata_rootfoldername")}/{f.get("metadata_foldername")}/{f.get("metadata_filename")}'
                file_map[path] = f

    return file_map


    def is_dir(self, path):
        return path in self.structure
        
    def is_file(self, path):
        return path in self.file_map
        
    def get_file(self, path):
        return self.file_map.get(path)
        
    def list_dir(self, path):
        return self.structure.get(path, [])
    
class FuseStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class TorBoxMediaCenterFuse(Fuse):
    def __init__(self, *args, **kwargs):
        super(TorBoxMediaCenterFuse, self).__init__(*args, **kwargs)

        threading.Thread(target=self.getFiles, daemon=True).start()

        self.files = []
        self.vfs = VirtualFileSystem(self.files)
        self.file_handles = {}
        self.next_handle = 1
        self.cached_links = {}

        self.cache = {}
        self.block_size = 1024 * 1024 * 64  # 64MB Blocks
        self.max_blocks = 64 # Max 64 blocks in cache (4GB)

    def getFiles(self):
        while True:
            files = getAllUserDownloads()
            if files:
                self.files = files
                self.vfs = VirtualFileSystem(self.files)
                logging.debug(f"Updated {len(self.files)} files in VFS")
            time.sleep(300)
        
    def getattr(self, path):
        st = FuseStat()
        now = int(time.time())
        st.st_atime = now
        st.st_mtime = now
        st.st_ctime = now
        
        st.st_uid = os.getuid()
        st.st_gid = os.getgid()
        
        if self.vfs.is_dir(path):
            st.st_mode = stat.S_IFDIR | 0o755
            st.st_nlink = 2
            return st
        elif self.vfs.is_file(path):
            file_info = self.vfs.get_file(path)
            if not file_info:
                return -errno.ENOENT
            st.st_mode = stat.S_IFREG | 0o444
            st.st_nlink = 1
            st.st_size = file_info.get('file_size', 0)
            return st
            
        # Not found
        return -errno.ENOENT
    
    def readdir(self, path, _):
        if not self.vfs.is_dir(path):
            return -errno.ENOENT
            
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')
        
        for item in self.vfs.list_dir(path):
            yield fuse.Direntry(item)
    
    def open(self, _, flags):
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES
    
    def read(self, path, size, offset):
        logging.debug(f"READ Path: {path}")
        logging.debug(f"READ Size: {size}")
        logging.debug(f"READ Offset: {offset}")
        file = self.vfs.get_file(path)

        if not file:
            return -errno.ENOENT
        
        current_time = time.time()
        if path not in self.cached_links:
            self.cached_links[path] = {
                'link': getDownloadLink(file.get('download_link')),
                'timestamp': current_time
            }
        elif current_time - self.cached_links[path]['timestamp'] > LINK_AGE:
            download_link = getDownloadLink(file.get('download_link'))
            self.cached_links[path] = {
                'link': download_link,
                'timestamp': current_time
            }
        download_link = self.cached_links[path]['link']
        
        start_block = offset // self.block_size
        end_block = (offset + size - 1) // self.block_size
        
        buffer = bytearray()
        
        for block_index in range(start_block, end_block + 1):
            block_offset = block_index * self.block_size
            block_end = min((block_index + 1) * self.block_size - 1, file.get('file_size') - 1)
            current_block_size = block_end - block_offset + 1
            
            # check for block
            if (path, block_index) not in self.cache:
                logging.debug(f"Cache miss for block {block_index}, fetching...")
                # get block
                block_data = downloadFile(download_link, current_block_size, block_offset)
                if not block_data:
                    return -errno.EIO
                # save block to cache
                self.cache[(path, block_index)] = block_data
                # lru cache
                if len(self.cache) > self.max_blocks * len(self.cached_links):
                    keys_to_remove = list(self.cache.keys())[:len(self.cache) - self.max_blocks]
                    for key in keys_to_remove:
                        del self.cache[key]
            # get block from cache
            block_data = self.cache[(path, block_index)]
            
            start_offset_in_block = max(0, offset - block_offset)
            end_offset_in_block = min(len(block_data), offset + size - block_offset)
            
            buffer.extend(block_data[start_offset_in_block:end_offset_in_block])
        
        return bytes(buffer)
    
    def release(self, _, fh):
        if fh in self.file_handles:
            del self.file_handles[fh]
        return 0
    
def runFuse():
    server = TorBoxMediaCenterFuse(
        version="%prog " + fuse.__version__,
        usage="%prog [options] mountpoint",
        dash_s_do="setsingle",
    )

    server.parser.add_option(
        mountopt="root",
        metavar="PATH",
        default=MOUNT_PATH,
        help="Mount point for the filesystem",
    )
    if platform != "darwin":
        server.fuse_args.add(
            "nonempty"
        )
    server.fuse_args.add(
        "allow_other"
    )
    server.fuse_args.add(
        "-f"
    )
    server.parse(values=server, errex=1)
    try:
        server.fuse_args.mountpoint = MOUNT_PATH
    except OSError as e:
        logging.error(f"Error changing directory: {e}")
        sys.exit(1)
    server.main()

def unmountFuse():
    try:
        os.system("fusermount -u " + MOUNT_PATH)
    except OSError as e:
        logging.error(f"Error unmounting: {e}")
        sys.exit(1)
    logging.info("Unmounted successfully.")
