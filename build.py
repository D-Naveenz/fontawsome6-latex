"""
Fontawesome 6 package build script - v1.0.1
Naveen Dharmathunga (dasheenaveen@outlook.com)
================================================================================
It may be distributed and/or modified under the
conditions of the LaTeX Project Public License, either version 1.3
of this license or (at your option) any later version.
================================================================================
Additionally, this derived work is licensed under the MIT License.
See LICENSE file in the root directory for more information.
"""

import os
import json

# download zip file from https://fontawesome.com/download and extract into fontawesome directory.
SOURCE_DIR = 'fontawesome'
OUTPUT_DIR = 'output'

OUTPUT_FILE = 'fontawesome6.sty'


# Read the icons.json file in the metadata folder
def get_icons_metadata() -> dict:
    input_file = os.path.join(SOURCE_DIR, "metadata", "icons.json")
    with open(input_file) as metadata_file:
        metadata = json.load(metadata_file)
        return metadata


# Read the header latex style file
def get_tex_header() -> str:
    input_file = 'fontawesome6.header.sty'
    with open(input_file) as header:
        return header.read()


def create_icons(metadata: dict) -> str:
    result = ''
    # Example: \faDefineIcon{apple}{\FABrands\symbol{"F179}} % U+F179: Apple
    output_template = \
        r'\faDefineIcon{{{name}}}{{{font}\symbol{{"{symbol}"}}}} % U+{symbol_filled}: {label}{term}'
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
            symbol=unicode,
            symbol_filled=unicode.zfill(4),
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build_style()
