from abc import ABC, abstractmethod
import os
from pathlib import Path
import platform
from typing import Optional

import py7zr


class FileAttributes:
    ReadOnly: bool
    """The item is read-only."""

    Directory: bool
    """The item is a directory."""

    Archive: bool
    """The item is archived."""

    Temporary: bool
    """The item is a temporary file."""

    LocallyIncomplete: bool
    """The item is locally incomplete. Windows only."""


class StorageIO(ABC):
    def __init__(self, name: str, root_path: Optional[Path] = None):
        # If a root path is not provided, use the local app data folder
        if root_path is not None and isinstance(root_path, Path):
            self.__path = root_path / name
        else:
            # Check whether the application is intended to save data locally
            if self.setup_local:
                self.__path = self.get_local_app_data_folder() / name
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
        attr = FileAttributes()
        if os.path.isdir(self.__path):
            attr.Directory = True
        else:
            # Check if the file is read-only
            if not os.access(self.__path, os.W_OK):
                attr.ReadOnly = True
            # Check if the file is a temporary file
            if self.__path.name.startswith("~") or self.__path.suffix in [
                ".tmp",
                ".temp",
            ]:
                attr.Temporary = True
            # Check if the file is archived
            if py7zr.is_7zfile(self.__path) or self.__path.suffix == ".zip":
                attr.Archive = True

        return attr

    @property
    def date_created(self) -> float:
        """Returns the creation date of the file or directory."""
        return os.path.getctime(self.__path)

    @classmethod
    def get_local_app_data_folder(cls) -> Path:
        system = platform.system()
        if system == "Windows":
            return Path(
                os.getenv("LOCALAPPDATA")
            )  # e.g., C:\Users\<User>\AppData\Local
        elif system == "Darwin":  # macOS
            return Path(os.path.expanduser("~/Library/Application Support"))
        elif system == "Linux":
            return Path(os.path.expanduser("~/.local/share"))
        else:
            raise NotImplementedError(f"Unsupported OS: {system}")

    @abstractmethod
    def read(self) -> bytes:
        """Reads data from the file."""
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """Writes data to the file."""
        pass

    @abstractmethod
    def delete(self) -> None:
        """Deletes the file."""
        pass


class StorageFolder(StorageIO):
    setup_local: bool = True

    def __init__(self, name: str, root_path: Optional[Path] = None):
        super().__init__(name, root_path)

        # make storage available
        self.__path.mkdir(parents=True, exist_ok=True)
