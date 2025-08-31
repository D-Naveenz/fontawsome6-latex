import os
from pathlib import Path
import platform
from core_structures import StorageModel, StorageFolder


def get_local_folder() -> Path:
    """Returns the local application data folder path based on the operating system."""
    system = platform.system()
    if system == "Windows":
        return Path(os.getenv("LOCALAPPDATA"))  # e.g., C:\Users\<User>\AppData\Local
    elif system == "Darwin":  # macOS
        return Path(os.path.expanduser("~/Library/Application Support"))
    elif system == "Linux":
        return Path(os.path.expanduser("~/.local/share"))
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")


__all__ = ["StorageModel", "StorageFolder", "get_local_folder"]
