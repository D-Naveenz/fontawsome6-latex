"""
Fontawesome 6 package build script - v1.0.1
Naveen Dharmathunga (dasheenaveen@outlook.com)
================================================================================
This work is licensed under the MIT License.
See LICENSE.txt file in the root directory for more information.
"""
import os
import shutil
import tempfile

from fontawesome import FontAwesome


# SOURCE_DIR = tempfile.TemporaryDirectory(prefix='fa6_')
OUTPUT_DIR = 'output\\fontawesome'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("==== Fontawesome 6 build script ====")
    # Clear the output folder
    # shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    # # Create output folders
    # os.makedirs(os.path.join(OUTPUT_DIR, 'fonts'), exist_ok=True)
    # os.makedirs(os.path.join(OUTPUT_DIR, 'licenses'), exist_ok=True)

    print("Cleaned the output directory.")

    fontawesome = FontAwesome()
    # Fetch the FontAwesome 6 download link and version
    download_link, version = fontawesome.fetch_data('https://fontawesome.com/download')
    print(f"FontAwesome {version} will be downloaded from {download_link}")
    
    # Build the fontawesome6.sty file
    fontawesome.build(SOURCE_DIR, OUTPUT_DIR)
    print("Successfully built fontawesome 6 package.")
