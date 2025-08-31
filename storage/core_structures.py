import asyncio
import re
from abc import ABC, abstractmethod
import os
from pathlib import Path
import shutil
import tarfile
from typing import Optional, override
import zipfile
import magic
from tqdm import tqdm

from storage import get_local_folder


class FileAttributes:
    ReadOnly: bool
    """The item is read-only."""

    Directory: bool
    """The item is a directory."""

    Archive: bool
    """The item is archived."""

    Temporary: bool
    """The item is a temporary file."""


def is_archive(file_path: str) -> bool:
    """
    Check if a file is a common archive format using a combination of:
    - Standard library modules (zipfile, tarfile)
    - MIME type detection
    - File signature checks for non-supported formats
    """
    if not os.path.isfile(file_path):
        return False

    # Check for ZIP files using standard library
    if zipfile.is_zipfile(file_path):
        return True

    # Check for TAR files (including compressed variants)
    try:
        if tarfile.is_tarfile(file_path):
            return True
    except Exception:
        pass

    # MIME type detection using python-magic
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)

        archive_mime_types = {
            "application/x-rar-compressed",
            "application/x-rar",
            "application/vnd.rar",
            "application/x-7z-compressed",
            "application/x-gzip",
            "application/x-bzip2",
            "application/x-xz",
            "application/zstd",
        }

        if mime_type in archive_mime_types:
            return True

        # Additional check for ZIP (some systems report different MIME types)
        if mime_type in ["application/zip", "application/x-zip-compressed"]:
            return True

    except ImportError:
        # Fallback to file signature if magic is not available
        return check_archive_signature(file_path)

    return False


def check_archive_signature(file_path: str) -> bool:
    """Fallback method using file signatures when python-magic is unavailable"""
    try:
        with open(file_path, "rb") as f:
            header = f.read(12)  # Read first 12 bytes for signature detection

        # ZIP: PK\x03\x04 or PK\x05\x06 (empty archive) or PK\x07\x08 (spanned)
        if (
            header.startswith(b"PK\x03\x04")
            or header.startswith(b"PK\x05\x06")
            or header.startswith(b"PK\x07\x08")
        ):
            return True

        # 7Z: '7z' magic number
        if header.startswith(b"7z\xbc\xaf\x27\x1c"):
            return True

        # RAR: Rar! magic number (v1.5-v5)
        if header.startswith(b"Rar!\x1a\x07\x00") or header.startswith(
            b"Rar!\x1a\x07\x01\x00"
        ):
            return True

        # GZIP: \x1f\x8b\x08
        if header.startswith(b"\x1f\x8b\x08"):
            return True

        # BZ2: BZh
        if header.startswith(b"BZh"):
            return True

        # XZ: \xFD7zXZ\x00
        if header.startswith(b"\xfd7zXZ\x00"):
            return True

        # ZSTD: \x28\xB5\x2F\xFD
        if header[:4] == b"\x28\xb5\x2f\xfd":
            return True

    except Exception:
        pass

    return False


def is_temp_file(file_path: str) -> bool:
    """
    Check if a file is likely a temporary file based on naming patterns and location.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file matches temporary file characteristics, False otherwise.
    """
    # Get the filename without directory path
    filename = os.path.basename(file_path)

    # Common temporary file patterns
    patterns = [
        r"^~\$.*",  # Office temp files (e.g., ~$document.docx)
        r"^~.*",  # Files starting with tilde (e.g., ~tempfile.txt)
        r".*\.tmp$",  # .tmp extension
        r".*\.temp$",  # .temp extension
        r".*\.crdownload$",  # Chrome partial downloads
        r".*\.part$",  # Firefox partial downloads
        r"^\._.*",  # macOS resource fork files
        r"^\.DS_Store$",  # macOS folder metadata
        r"^desktop\.ini$",  # Windows folder metadata
        r".*\.bak$",  # Backup files
        r".*\.dmp$",  # Memory dump files
        r"^Thumbs\.db$",  # Windows thumbnail cache
    ]

    # Check filename against patterns
    for pattern in patterns:
        if re.match(pattern, filename, re.IGNORECASE):
            return True

    # Check if in system temp directories
    temp_dirs = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        os.environ.get("TMPDIR", ""),
        "/tmp",
        "/var/tmp",
        "~/temp",
        "~/tmp",
        "/private/var/folders",  # macOS temp location
    ]

    # Normalize paths for comparison
    abs_path = os.path.abspath(file_path)
    for temp_dir in temp_dirs:
        if not temp_dir:
            continue
        expanded_dir = os.path.abspath(os.path.expanduser(temp_dir))
        if abs_path.startswith(expanded_dir + os.sep):
            return True

    return False


class StorageModel(ABC):
    setup_local: bool = True

    def __init__(self, name: str, root_path: Optional[Path] = None):
        # Initialize the object with empty attributes
        self.__attributes = self.__get_attributes()

        # If a root path is not provided, use the local app data folder
        if root_path is not None and isinstance(root_path, Path):
            self.__path = root_path / name
        else:
            # Check whether the application is intended to save data locally
            if self.setup_local:
                self.__path = get_local_folder() / name
            else:
                # Use the location of main.py
                self.__path = os.path.abspath(__file__) / name

    @property
    def path(self) -> Path:
        """The full path of the current folder in the file system, if the path is available."""
        return self.__path

    @property
    def name(self) -> str:
        """The name of the current folder."""
        return self.__path.name

    @property
    def attributes(self) -> FileAttributes:
        """Returns the attributes of the file or directory."""
        return self.__attributes

    @property
    def date_created(self) -> float:
        """Returns the creation date of the file or directory."""
        return os.path.getctime(self.__path)

    async def _copy_file(
        self, new_path: Path, semaphore: asyncio.Semaphore, pbar: tqdm
    ) -> None:
        """Asynchronously copy a single file with progress tracking."""
        async with semaphore:  # Limit concurrent copies
            loop = asyncio.get_running_loop()
            try:
                # Run blocking I/O in a thread
                await loop.run_in_executor(None, shutil.copy2, self.__path, new_path)
            except Exception as e:
                print(f"\nError copying {self.__path}: {e}")
            finally:
                pbar.update(1)  # Update progress bar

    async def _move_file(
        self, new_path: Path, semaphore: asyncio.Semaphore, pbar: tqdm
    ) -> None:
        """Asynchronously move a single file with progress tracking."""
        async with semaphore:  # Limit concurrent moves
            loop = asyncio.get_running_loop()
            try:
                # Run blocking I/O in a thread
                await loop.run_in_executor(None, shutil.move, self.__path, new_path)
            except Exception as e:
                print(f"\nError moving {self.__path}: {e}")
            finally:
                pbar.update(1)  # Update progress bar

    async def delete_file(file_path: str, pbar: tqdm) -> None:
        """Asynchronously delete a single file with progress tracking."""
        try:
            await asyncio.to_thread(os.remove, file_path)
        except Exception as e:
            print(f"\nError deleting {file_path}: {e}")
        finally:
            pbar.update(1)  # Update progress bar after deletion attempt

    async def rename_async(self, new_name: str) -> None:
        """
        Renames the current file or directory to a new name asynchronously.

        Args:
            new_name: The new name for the file or directory.
        """
        new_path = self.__path.parent / new_name
        await asyncio.to_thread(os.rename, self.__path, new_path)
        self.__path = new_path
        self.__attributes = self.__get_attributes()

    @abstractmethod
    async def copy_async(self, new_path: Path, **kwargs) -> None:
        """
        Copies the current file or directory to a new path asynchronously.

        Args:
            new_path: The new path where the file or directory should be copied.
        """
        pass

    @abstractmethod
    async def move_async(self, new_path: Path, **kwargs) -> None:
        """
        Moves the current file or directory to a new path asynchronously.

        Args:
            new_path: The new path where the file or directory should be moved.
        """
        pass

    @abstractmethod
    async def delete_async(self, **kwargs) -> None:
        """Deletes the current file or directory asynchronously."""
        pass

    def __get_attributes(self) -> FileAttributes:
        attr = FileAttributes()
        if os.path.isdir(self.__path):
            attr.Directory = True
        else:
            # Check if the file is read-only
            attr.ReadOnly = not os.access(self.__path, os.W_OK)
            # Check if the file is a temporary file
            attr.Temporary = is_temp_file(self.__path)
            # Check if the file is archived
            attr.Archive = is_archive(self.__path)

        return attr


class StorageFolder(StorageModel):
    def __init__(self, name: str, root_path: Optional[Path] = None):
        # Make sure the root path is a directory
        if root_path is not None and not os.path.isdir(root_path):
            # Remove the file from the path if it exists
            root_path = root_path.parent

        super().__init__(name, root_path)

        # make storage available
        self.__path.mkdir(parents=True, exist_ok=True)

    def __collect_files_and_dirs(self) -> tuple[list[str], list[str]]:
        """
        Traverse directory and return relative paths of all files/dirs.
        """
        all_files = []
        all_dirs = []
        for root, dirs, files in os.walk(self.__path):
            rel_root = os.path.relpath(root, self.__path)
            if rel_root == ".":  # Handle root directory
                all_dirs.extend(dirs)
                all_files.extend(files)
            else:
                all_dirs.extend(os.path.join(rel_root, d) for d in dirs)
                all_files.extend(os.path.join(rel_root, f) for f in files)
        return all_dirs, all_files

    @override
    async def copy_async(self, new_path: Path, *, max_concurrent=100, **kwargs) -> None:
        """
        Copies the current folder to a new location asynchronously.

        Args:
            new_path: The new path where the folder should be copied.
            max_concurrent: The maximum number of concurrent copy operations.
        """
        dst = os.path.abspath(new_path)

        if not os.path.exists(dst):
            os.makedirs(dst, exist_ok=True)

        # Collect all directories and files
        all_dirs, all_files = await asyncio.to_thread(self.__collect_files_and_dirs)

        # Create destination directories
        for rel_dir in all_dirs:
            os.makedirs(os.path.join(dst, rel_dir), exist_ok=True)

        # Setup progress bar and semaphore
        with tqdm(total=len(all_files), unit="file", desc="Copying") as pbar:
            sem = asyncio.Semaphore(max_concurrent)
            tasks = []
            for rel_file in all_files:
                src_path = os.path.join(self.__path, rel_file)
                dst_path = os.path.join(dst, rel_file)
                task = asyncio.create_task(
                    self._copy_file(src_path, dst_path, sem, pbar)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def move_async(self, new_path: Path, *, max_concurrent=100, **kwargs) -> None:
        """
        Moves the current folder to a new location asynchronously.

        Args:
            new_path: The new path where the folder should be moved.
            max_concurrent: The maximum number of concurrent move operations.
        """
        dst = os.path.abspath(new_path)

        if not os.path.exists(dst):
            os.makedirs(dst, exist_ok=True)

        # Collect all directories and files
        all_dirs, all_files = await asyncio.to_thread(self.__collect_files_and_dirs)

        # Create destination directories
        for rel_dir in all_dirs:
            os.makedirs(os.path.join(dst, rel_dir), exist_ok=True)

        # Setup progress bar and semaphore
        with tqdm(total=len(all_files), unit="file", desc="Moving") as pbar:
            sem = asyncio.Semaphore(max_concurrent)
            tasks = []
            for rel_file in all_files:
                src_path = os.path.join(self.__path, rel_file)
                dst_path = os.path.join(dst, rel_file)
                task = asyncio.create_task(
                    self._move_file(src_path, dst_path, sem, pbar)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def delete_async(self, **kwargs) -> None:
        """Deletes the current folder asynchronously."""
        # Collect all directories and files
        _, all_files = await asyncio.to_thread(self.__collect_files_and_dirs)

        # Setup progress bar
        with tqdm(total=len(all_files), unit="file", desc="Deleting") as pbar:
            tasks = []
            for rel_file in all_files:
                file_path = os.path.join(self.__path, rel_file)
                task = asyncio.create_task(self.delete_file(file_path, pbar))
                tasks.append(task)
            await asyncio.gather(*tasks)

        # Finally, remove empty directories
        for root, dirs, _ in os.walk(self.__path, topdown=False):
            for d in dirs:
                dir_path = os.path.join(root, d)
                try:
                    os.rmdir(dir_path)
                except OSError:
                    pass
