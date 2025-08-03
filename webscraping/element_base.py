from playwright.async_api import Locator, Page, Position
from typing import Dict, Literal, Optional, Pattern, Sequence, Union


class ElementBase:
    def __init__(self, locator: Union[Locator, str], page: Page):
        if isinstance(locator, str):
            self.__locator = page.locator(locator)
        else:
            self.__locator = locator

    def __init__(self, parent: Union[Locator, Page]):
        self.__locator = parent

    @property
    def page(self) -> Page:
        """
        A page this locator belongs to.

        Returns
        -------
        Page
        """
        return (
            self.__locator.page
            if isinstance(self.__locator, Locator)
            else self.__locator
        )

    @property
    def locator(self) -> Union[Locator, Page]:
        """
        Returns the locator for this element.

        Returns:
            Union[Locator, Page]: The locator for this element.
        """
        return self.__locator

    @property
    async def text(self) -> str:
        """
        Returns the text content of the element.

        Returns:
            str: The text content of the element.
        """
        return await self.__locator.text_content() or ""

    @property
    async def content(self) -> str:
        """
        Returns the inner HTML content of the element.

        Returns:
            str: The inner HTML content of the element.
        """
        return await self.__locator.inner_html() or ""

    async def get_attribute(self, attribute: str) -> Optional[str]:
        return await self.__locator.get_attribute(attribute)

    async def is_visible(self) -> bool:
        return await self.__locator.is_visible()
