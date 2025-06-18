from enum import Enum
from typing import Awaitable, Callable, TypeVar, Union
from playwright.async_api import async_playwright, Page, Browser
from playwright._impl._errors import Error as PlaywrightError

T = TypeVar("T")  # Generic return type


class BrowserType(Enum):
    DEFAULT = None
    CHROME = "chrome"
    MS_EDGE = "msedge"


class WebBrowser:
    def __init__(
        self, browser: BrowserType = BrowserType.DEFAULT, headless: bool = True
    ):
        self.browser_type = browser
        self.headless = headless

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.__get_browser_connection()
        return self

    async def __aexit__(self, *args):
        await self.browser.close()
        await self.playwright.stop()

    def __str__(self):
        return f"WebScraper(browser={self.browser_type}, headless={self.headless})"

    async def __get_browser_connection(self) -> Union[Browser, None]:
        """
        Establish a connection to the browser.

        Returns:
            An instance of the browser. If the specified browser fails, it falls back to the default browser.
        """
        try:
            # Try to launch the configured browser
            return await self.playwright.chromium.launch(
                channel=self.browser_type.value, headless=self.headless
            )
        except PlaywrightError:
            try:
                # Fallback to default browser if specified browser fails
                return await self.playwright.chromium.launch(headless=self.headless)
            except PlaywrightError as e:
                # Handle any errors that occur while launching the browser
                print(f"Error getting browser: {e}")
                return None

    async def scrape(self, url: str, handler: Callable[[Page], Awaitable[T]]) -> T:
        """
        Open a page, pass it to a handler function, and return the result.

        Args:
            url (str): The URL to load.
            handler (Callable[[Page], Awaitable[T]]): A coroutine function that operates on the page.

        Returns:
            T: The result returned by the handler function.
        """
        try:
            page = await self.browser.new_page()
            await page.goto(url, timeout=10000)  # Timeout in ms
            return await handler(page)  # Pass the page to your custom function
        except Exception as e:
            print(f"Error during scraping: {e}")
            return None
