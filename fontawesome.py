import os
import re

import requests

from tex_builder import TexBuilder
from web_page import WebPage


class FontAwesome:
    FONTAWESOME_URL = 'https://fontawesome.com/download' # URL to download FontAwesome Web Page
    LINK_PATTERN = r'fontawesome-(\w+)-(\d+\.\d+\.\d+)-desktop\.zip'
    
    def __init__(self):
        self.version: str | None = None
        self.download_link: str | None = None

    def _is_link_matching(self, link):
        # get the last part of the link
        # last_part = link.split('/')[-1]

        # Check if the last part matches the pattern
        if re.match(self.LINK_PATTERN, link):
            return True
        return False

    def _get_fa6_link(self, url):
        # Element to find the download link for FontAwesome 6
        # <a href="https://use.fontawesome.com/releases/v6.7.2/fontawesome-free-6.7.2-desktop.zip" class="button text-capitalize tablet:margin-left-xl">
        #   <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="arrow-down-to-line" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" class="margin-right-2xs svg-inline--fa fa-arrow-down-to-line fa-lg"><path fill="currentColor" d="M32 480c-17.7 0-32-14.3-32-32s14.3-32 32-32l320 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 480zM214.6 342.6c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 242.7 160 64c0-17.7 14.3-32 32-32s32 14.3 32 32l0 178.7 73.4-73.4c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3l-128 128z" class=""></path></svg>
        #   Free for desktop
        # </a>
        webpage = WebPage(url)
        target_elements = webpage.content.get_by_role('link', name='Free for desktop').inner_html()
        for element in target_elements:
            if 'href' in element.attrs and self._is_link_matching(element['href']):
                return element['href']
        return None

    def _get_fa6_version(self, download_link):
        # Extract the version from the download link
        match = re.search(self.LINK_PATTERN, download_link)
        if match:
            return match.group(2)
        return None
    
    def fetch_data(self, url):
        """
        Fetch the FontAwesome 6 download link and version from the given URL.
        
        Args:
            url (str): The URL to fetch the FontAwesome 6 data from.
        
        Returns:
            tuple: A tuple containing the download link and version, or None if not found.
        """
        self.download_link = self._get_fa6_link(url)
        if not self.download_link:
            print("Error: Could not find the download link for FontAwesome 6.")
            return None, None

        self.version = self._get_fa6_version(self.download_link)
        return self.download_link, self.version

    def download(self, destination_dir):
        # Get the download link for FontAwesome 6
        if not self.download_link:
            print("Error: Could not find the download link for FontAwesome 6.")
            return False

        # Download the file
        print(f"Downloading FontAwesome 6 from {self.download_link}...")
        try:
            response = requests.get(self.download_link, stream=True)
            response.raise_for_status()  # Raise an error for HTTP errors
            with open(os.path.join(destination_dir, 'fontawesome.zip'), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download completed.")
            return True
        except requests.RequestException as e:
            print(f"Error downloading FontAwesome 6: {e}")
            return False
    
    def build(self, source_dir, output_dir):
        """
        Build the FontAwesome 6 LaTeX package from the downloaded files.
        
        Args:
            source_dir (str): The directory containing the downloaded FontAwesome files.
            output_dir (str): The directory where the LaTeX package will be built.
        
        Returns:
            bool: True if the build was successful, False otherwise.
        """
        tex_builder = TexBuilder(source_dir=source_dir, output_dir=output_dir)
        tex_builder.build()

        return True