"""
Fontawesome 6 package build script - v1.0.1
Naveen Dharmathunga (dasheenaveen@outlook.com)
================================================================================
This work is licensed under the MIT License.
See LICENSE.txt file in the root directory for more information.
"""
import glob
import os
import json
import re
import shutil


SOURCE_DIR = 'fontawesome'
OUTPUT_DIR = 'output\\fontawesome'
OUTPUT_FILE = '6.sty'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("==== Fontawesome 6 build script ====")
    # Clear the output folder
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    # Create output folders
    os.makedirs(os.path.join(OUTPUT_DIR, 'fonts'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'licenses'), exist_ok=True)

    print("Cleaned the output directory.")

    # Build the fontawesome6.sty file
    print("Building fontawesome 6 package...")
    build_style()

    # Copy other files
    print("Copying files...")
    copy_other()

    print("Successfully built fontawesome 6 package.")
