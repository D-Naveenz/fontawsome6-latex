"""
Fontawesome 6 package build script - v1.0.1
Naveen Dharmathunga (dasheenaveen@outlook.com)
================================================================================
This work is licensed under the MIT License.
See LICENSE.txt file in the root directory for more information.
"""
import asyncio
import glob
import os
import json
import shutil

from pathlib import Path

import download as dl

# download zip file from https://fontawesome.com/download and extract into fontawesome directory.
SITE_URL = "https://fontawesome.com/download"
CWD = Path(__file__).parent
FONT_DIR = Path(CWD, 'font')
OUTPUT_DIR = Path(CWD).parent


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("==== Fontawesome 6 build script ====")
    
    # Step 1: Download the zip file
    download_link = asyncio.run(dl.get_download_url_async(SITE_URL))
    
    if download_link:
        print(f"Download link found: {download_link}")

        # Step 2: Download the file
        save_path = "fontawesome-desktop.zip"
        dl.download_file(download_link, save_path, num_threads=4)
    else:
        print("Download link not found.")
