import requests
from bs4 import BeautifulSoup


class WebPage:
    """
    A class to represent a web page.
    """
    def __init__(self, url):
        self.url = url
        self.content = None
        
        # Fetch and Parse the content immediately upon initialization
        self._parse_content(self._fetch())

    def __str__(self):
        return f"WebPage for {self.url} with content length: {len(self.content) if self.content else 0}"

    def _fetch(self):
        """
        Fetch the raw HTML content from the specified URL.
        Raises:
            Exception: If the request fails or the status code is not 200.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch content from {self.url}")
        
    def _parse_content(self, raw_content=None):
        """
        Parse the fetched HTML content.
        Raises:
            Exception: If no content has been fetched.
        """
        if not raw_content:
            raise Exception("No content fetched to parse.")
        soup = BeautifulSoup(raw_content, 'html.parser')
        self.content = soup
        return soup
        
    def pretty_out(self):
        """
        Return a prettified version of the parsed HTML content.
        Raises:
            Exception: If no content has been parsed.
        """
        if not self.content:
            raise Exception("No content parsed to prettify.")
        return self.content.prettify()
    
    def get_element_by_id(self, element_id):
        """
        Get an HTML element by its ID.
        Args:
            element_id (str): The ID of the HTML element to retrieve.
        Returns:
            bs4.element.Tag: The HTML element with the specified ID, or None if not found.
        """
        if not self.content:
            raise Exception("No content parsed to search for elements.")
        return self.content.find(id=element_id)
    
    def get_elements(self, tag_name, class_name=None):
        """
        Get all HTML elements by tag name and optional class name.
        Args:
            tag_name (str): The tag name of the HTML elements to retrieve.
            class_name (str, optional): The class name to filter the elements. Defaults to None.
        Returns:
            list: A list of HTML elements matching the specified tag name and class name.
        """
        if not self.content:
            raise Exception("No content parsed to search for elements.")
        if class_name:
            return self.content.find_all(tag_name, class_=class_name)
        return self.content.find_all(tag_name)
