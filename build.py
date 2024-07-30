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
import shutil

# download zip file from https://fontawesome.com/download and extract into fontawesome directory.
SOURCE_DIR = 'fontawesome'
OUTPUT_DIR = 'output\\fontawesome'
OUTPUT_FILE = '6.sty'


# Read the icons.json file in the metadata folder
def get_icons_metadata() -> dict:
    input_file = os.path.join(SOURCE_DIR, "metadata", "icons.json")
    with open(input_file) as metadata_file:
        metadata = json.load(metadata_file)
        return metadata


# Read the header latex style file
def get_tex_header() -> str:
    input_file = 'header.sty'
    with open(input_file) as header:
        return header.read()


def create_icons(metadata: dict) -> str:
    result = ''
    # Example: \faDefineIcon{apple}{\FABrands\symbol{"F179}} % U+F179: Apple
    output_template = \
        r'\faDefineIcon{{{name}}}{{{font}\symbol{{"{symbol}}}}} % U+{symbol}: {label}{term}'
    for icon_name in sorted(metadata.keys()):
        font = r"\FA" if "brands" not in metadata[icon_name]["styles"] else r"\FABrands"
        unicode = metadata[icon_name]["unicode"].upper()
        label = metadata[icon_name].get("label", "")
        try:
            term = ' [' + metadata[icon_name]["search"]["terms"][0] + ']'
        except IndexError:
            term = ''

        # write the output line and push it to the result
        output_line = output_template.format(
            name=icon_name,
            font=font,
            symbol=unicode.zfill(4),
            label=label,
            term=term
        )
        result += output_line + '\n'
    return result


def build_style():
    output_file = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_file, 'w') as style:
        # write the header
        style.write(get_tex_header())
        style.write('\n')

        # write icon definitions
        style.write(create_icons(get_icons_metadata()))

        # write the ending line
        style.write(r'\endinput')


def copy_other():
    # Copy fonts
    files = glob.glob(os.path.join(SOURCE_DIR, 'otfs') + '\\Font Awesome 6 *')
    output_dir = os.path.join(OUTPUT_DIR, 'fonts')
    for file in files:
        filename = os.path.basename(file)
        try:
            shutil.copy2(file, output_dir)
            print(f'Copied {filename} to {output_dir}')
        except PermissionError as e:
            print(f"Failed to copy file: {filename}, Stacktrace: {e}")

    # Copy licenses
    files = glob.glob('licenses\\*')
    output_dir = os.path.join(OUTPUT_DIR, 'licenses')
    for file in files:
        filename = os.path.basename(file)
        try:
            shutil.copy2(file, output_dir)
            print(f'Copied {filename} to {output_dir}')
        except PermissionError as e:
            print(f"Failed to copy file: {filename}, Stacktrace: {e}")

    # Copy files in the root directory
    try:
        shutil.copy2('README.md', OUTPUT_DIR)
        print(f'Copied readme to {OUTPUT_DIR}')
        shutil.copy2('LICENSE.txt', OUTPUT_DIR)
        print(f'Copied license to {OUTPUT_DIR}')
    except PermissionError as e:
        print(f"Failed to copy README.md, Stacktrace: {e}")


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
