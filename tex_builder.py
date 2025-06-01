import fnmatch
import glob
import json
import os
import re
import shutil


class TexBuilder:
    OUTPUT_FILE = 'fontawesome6.sty'
    HEADER_FILE = 'header.sty'
    
    def __init__(self, source_dir='source', output_dir='output'):
        self.source_dir = source_dir
        self.output_dir = output_dir
        
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        # Ensure the source directory is set
        self._validate_source()
        
        # Load metadata
        self.icons_metadata = self._get_icons_metadata(os.path.join(self.source_dir, 'metadata', 'icons.json'))

    def __str__(self):
        return f"TexBuilder(target={self.OUTPUT_FILE}, source={self.source_dir}, output={self.output_dir})"

    def _validate_source(self):
        # Check if the source directory exists and contains required files
        if not os.path.exists(self.source_dir):
            print(f"Error: The source directory {self.source_dir} does not exist.")
            return False
        
        # Check the fontawesome folder contains the required files
        target_files = [self.metadata_file, 'otfs/*.otf', 'license.txt']
        for target in target_files:
            if not any(os.path.exists(os.path.join(self.source_dir, f)) for f in glob.glob(os.path.join(self.source_dir, target))):
                print(f"Error: Required file {target} not found in source directory.")
                return False
        
        return True

    def _get_icons_metadata(self, filepath):
        try:
            with open(filepath) as metadata_file:
                metadata: dict = json.load(metadata_file)
                print(f"Loaded metadata from {filepath}")
                return metadata
        except FileNotFoundError:
            print(f"Error: The file {filepath} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file {filepath} is not a valid JSON file.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _get_tex_header(self):
        try:
            with open(os.path.join(self.source_dir, self.HEADER_FILE), 'r') as header_file:
                header_content = header_file.read()
                print(f"Loaded LaTeX header from {self.HEADER_FILE}")
                return header_content
        except FileNotFoundError:
            print(f"Error: The file {self.HEADER_FILE} does not exist in the source directory.")
        except Exception as e:
            print(f"An error occurred while reading the header file: {e}")

    def _create_icons(self, icons_metadata: dict):
        """
        Create LaTeX commands for Font Awesome icons.

        Args:
            icons_metadata (dict): A dictionary containing metadata for each icon.

        Returns:
            str: A string containing LaTeX commands for all icons.
        """
        icons = []
        for icon in sorted(icons_metadata.keys()):
            font = r"\FA" if "brands" not in icons_metadata[icon]["styles"] else r"\FABrands"
            unicode = icons_metadata[icon]["unicode"].upper()
            label = icons_metadata[icon].get("label", "")
            try:
                term = ' [' + icons_metadata[icon]["search"]["terms"][0] + ']'
            except IndexError:
                term = ''
            
            # write the output line and push it to the result
            # Template: \faDefineIcon{apple}{\FABrands\symbol{"F179}} % U+F179: Apple
            icons.append(
                r'\faDefineIcon{{{name}}}{{{font}{{\symbol{{"{symbol}}}}}}} % U+{symbol}: {label}{term}'.format(
                    name=icon,
                    font=font,
                    symbol=unicode.zfill(4),
                    label=label,
                    term=term
                )
            )
        
        # Join all icons into a single string
        return '\n'.join(icons)
        
    def create_tex_package(self, tex_file='document.sty'):
        """
        Create a LaTeX package file for Font Awesome icons.

        Args:
            tex_file (str, optional): The name of the LaTeX package file. Defaults to 'document.sty'.
        """
        # Ensure the tex file has ".sty" extension
        if not tex_file.endswith('.sty'):
            tex_file += '.sty'

        output_file = os.path.join(self.output_dir, tex_file)

        with open(output_file, 'w') as tex:
            # Write the header
            tex.write(self._get_tex_header())
            tex.write('\n')
            
            # Write icon definitions
            tex.write(self._create_icons(self.icons_metadata))
            
            # Write the ending line
            tex.write(r'\endinput')

        print(f"Tex package file created at: {output_file}")
        
    def copy_files(self, target_pattern: str, output_path: str = "./", ignore_case: bool = False, recursive: bool = False):
        """
        Copy files from the source directory to the output directory based on a pattern.
        
        Args:
            target_pattern (str): The glob pattern to match files in the source directory.
            output_path (str, optional): The relative path to copy files to. Defaults to the current directory.
            ignore_case (bool): Whether to perform case-insensitive matching.
            recursive (bool): Whether to search recursively in subdirectories.

        Returns:
            List[str]: List of paths that were successfully copied.
        """
        copied_files = []
        full_output_path = os.path.join(self.output_dir, output_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(full_output_path, exist_ok=True)
        
        # Handle case-insensitive matching
        if ignore_case:
            # Convert pattern to case-insensitive regex
            pattern_re = fnmatch.translate(target_pattern)
            pattern_re = "(?i)" + pattern_re  # Case-insensitive flag
            pat = re.compile(pattern_re)
            
            # Find all files and filter with regex
            all_files = glob.iglob(os.path.join(self.source_dir, "**" if recursive else "*"), recursive=recursive)
            files = [f for f in all_files if pat.search(os.path.basename(f))]
        else:
            files = glob.iglob(os.path.join(self.source_dir, target_pattern), recursive=recursive)
        
        # Copy files
        for file in files:
            if not os.path.isfile(file):  # Skip directories
                continue
                
            filename = os.path.basename(file)
            dest_path = os.path.join(full_output_path, filename)
            
            try:
                shutil.copy2(file, dest_path)  # copy2 preserves metadata
                copied_files.append(dest_path)
                print(f'Copied {filename} to {dest_path}')
            except OSError as e:
                print(f"Error copying {filename}: {e}")
        
        return copied_files
        

    def build(self):
        """
        Build the LaTeX package and copy necessary files.
        """
        
        tex_header = self._get_tex_header()
        if tex_header is None:
            return

        if not self.icons_metadata:
            return

        # Create the LaTeX package
        self.create_tex_package(self.OUTPUT_FILE)
        
        # Copy other necessary files
        try:
            self.copy_files(
                os.path.join(self.source_dir, 'otfs') + '\\Font Awesome 6 *', 
                "fonts") # Fonts
            self.copy_files(os.path.join(self.source_dir, '*.txt'), "licenses") # Font Awesome License
            self.copy_files('**/license.txt', "licenses", ignore_case=True, recursive=True)  # Package Licenses
            self.copy_files('README.md') # Readme
        except Exception as e:
            print(f"An error occurred while copying files: {e}")
