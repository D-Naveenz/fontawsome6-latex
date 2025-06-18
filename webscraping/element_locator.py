from playwright.async_api import Locator, Page
from typing import Optional, Pattern, Union


class ElementLocator:
    """
    A helper class for locating web elements using Playwright with a more intuitive interface
    that maps common HTML element names to their corresponding ARIA roles.

    This class provides a more familiar API for developers who are accustomed to working with
    HTML tags rather than ARIA roles. It wraps Playwright's locator methods while maintaining
    chainability and adding convenience methods for common element types.

    Key Features:
    - Wraps Playwright's get_by_role() with HTML-friendly method names
    - Returns ElementLocator instances for method chaining
    - Provides access to the underlying Locator/Page via the content property
    - Includes CSS selector support alongside role-based location
    - Comprehensive parameter support for each element type

    Usage:
        locator = ElementLocator(page)
        await locator.button("Submit").click()
        await locator.textbox("Username").fill("user123")

        # Chaining example:
        form = await locator.form("LoginForm")
        await form.textbox("Username").fill("user123")
        await form.textbox("Password").fill("pass123")
        await form.button("Submit").click()
    """

    def __init__(self, parent: Union[Locator, Page]):
        self.__framework_element = parent

    @property
    def content(self) -> Union[Locator, Page]:
        """
        Returns the underlying framework element (Locator or Page).
        This is useful for chaining further actions or locators.
        """
        return self.__framework_element

    async def find_by_selector(
        self, class_name: Optional[str] = None, id_name: Optional[str] = None
    ) -> "ElementLocator":
        """
        Locates an element by CSS selector. (The class name or the ID of the element can be used as a selector.)

        Args:
            class_name: The class name of the element
            id_name: The ID of the element

        Returns:
            Locator for the element

        Raises:
            ValueError: If neither class_name nor id_name is provided
        """
        selector = ""
        if class_name and id_name:
            selector = f".{class_name}#{id_name}"
        elif class_name:
            selector = f".{class_name}"
        elif id_name:
            selector = f"#{id_name}"
        else:
            raise ValueError("Either class_name or id_name must be provided")

        return ElementLocator(self.__framework_element.locator(selector))

    async def find_by_text(
        self, name: Union[str, Pattern], exact: bool = False
    ) -> Locator:
        """
        Locates text content (generic text elements).

        Args:
            name: Text content to find
            exact: Whether to match exactly

        Returns:
            Locator for the text element
        """
        return self.__framework_element.get_by_text(name, exact=exact)

    async def button(
        self, name: Optional[str] = None, disabled: bool = False, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a button element. Matches both <button> elements and elements with role="button".

        Args:
            name: Text content or accessible name of the button (optional)
            disabled: Whether the button is disabled
            exact: Whether to match name exactly (case-sensitive, whole-string)

        Returns:
            Locator for the button element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "button", name=name, disabled=disabled, exact=exact
            )
        )

    async def link(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a link (<a> element).

        Args:
            name: Visible text or accessible name of the link (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the link element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("link", name=name, exact=exact)
        )

    async def heading(
        self,
        name: Optional[str] = None,
        level: Optional[int] = None,
        exact: bool = False,
    ) -> "ElementLocator":
        """
        Locates a heading element (h1-h6).

        Args:
            name: Text content of the heading (optional)
            level: Heading level (1-6)
            exact: Whether to match name exactly

        Returns:
            Locator for the heading element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "heading", name=name, level=level, exact=exact
            )
        )

    async def textbox(
        self, name: Optional[str] = None, disabled: bool = False, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a text input element (<input type="text">, <textarea>, or role="textbox").

        Args:
            name: Accessible name (usually from associated label) (optional)
            disabled: Whether the textbox is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the text input element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "textbox", name=name, disabled=disabled, exact=exact
            )
        )

    async def checkbox(
        self,
        name: Optional[str] = None,
        checked: Optional[bool] = None,
        disabled: bool = False,
        exact: bool = False,
    ) -> "ElementLocator":
        """
        Locates a checkbox element (<input type="checkbox"> or role="checkbox").

        Args:
            name: Accessible name (usually from associated label) (optional)
            checked: Whether the checkbox is checked (None for don't care)
            disabled: Whether the checkbox is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the checkbox element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "checkbox", name=name, checked=checked, disabled=disabled, exact=exact
            )
        )

    async def radio(
        self,
        name: Optional[str] = None,
        checked: Optional[bool] = None,
        disabled: bool = False,
        exact: bool = False,
    ) -> "ElementLocator":
        """
        Locates a radio button element (<input type="radio"> or role="radio").

        Args:
            name: Accessible name (usually from associated label) (optional)
            checked: Whether the radio is selected (None for don't care)
            disabled: Whether the radio is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the radio button element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "radio", name=name, checked=checked, disabled=disabled, exact=exact
            )
        )

    async def select(
        self, name: Optional[str] = None, disabled: bool = False, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a select element (<select> or role="combobox").

        Args:
            name: Accessible name (usually from associated label) (optional)
            disabled: Whether the select is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the select element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "combobox", name=name, disabled=disabled, exact=exact
            )
        )

    async def image(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates an image element (<img> or role="img").

        Args:
            name: Alt text or accessible name of the image (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the image element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("img", name=name, exact=exact)
        )

    async def listitem(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a list item element (<li> or role="listitem").

        Args:
            name: Text content of the list item (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the list item element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("listitem", name=name, exact=exact)
        )

    async def table(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a table element (<table> or role="table").

        Args:
            name: Accessible name of the table (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the table element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("table", name=name, exact=exact)
        )

    async def cell(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a table cell element (<td> or role="cell").

        Args:
            name: Text content of the cell (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the table cell element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("cell", name=name, exact=exact)
        )

    async def text(
        self, name: Union[str, Pattern], exact: bool = False
    ) -> "ElementLocator":
        """
        Locates text content (generic text elements).

        Args:
            name: Text content to find
            exact: Whether to match exactly

        Returns:
            Locator for the text element
        """
        return ElementLocator(self.__framework_element.get_by_text(name, exact=exact))

    async def div(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a div element (generic container).

        Args:
            name: Text content or accessible name (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the div element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("generic", name=name, exact=exact)
        )

    async def paragraph(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a paragraph element (<p> or role="paragraph").

        Args:
            name: Text content of the paragraph (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the paragraph element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("paragraph", name=name, exact=exact)
        )

    async def form(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a form element (<form> or role="form").

        Args:
            name: Accessible name of the form (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the form element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("form", name=name, exact=exact)
        )

    async def heading(
        self, name: Optional[str], level: Optional[int] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a heading element (h1-h6).

        Args:
            name: Text content of the heading
            level: Heading level (1-6)
            exact: Whether to match name exactly

        Returns:
            Locator for the heading element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "heading", name=name, level=level, exact=exact
            )
        )

    async def textbox(
        self, name: str, disabled: bool = False, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a text input element (<input type="text">, <textarea>, or role="textbox").

        Args:
            name: Accessible name (usually from associated label)
            disabled: Whether the textbox is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the text input element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "textbox", name=name, disabled=disabled, exact=exact
            )
        )

    async def checkbox(
        self,
        name: str,
        checked: Optional[bool] = None,
        disabled: bool = False,
        exact: bool = False,
    ) -> "ElementLocator":
        """
        Locates a checkbox element (<input type="checkbox"> or role="checkbox").

        Args:
            name: Accessible name (usually from associated label)
            checked: Whether the checkbox is checked (None for don't care)
            disabled: Whether the checkbox is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the checkbox element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "checkbox", name=name, checked=checked, disabled=disabled, exact=exact
            )
        )

    async def radio(
        self,
        name: str,
        checked: Optional[bool] = None,
        disabled: bool = False,
        exact: bool = False,
    ) -> "ElementLocator":
        """
        Locates a radio button element (<input type="radio"> or role="radio").

        Args:
            name: Accessible name (usually from associated label)
            checked: Whether the radio is selected (None for don't care)
            disabled: Whether the radio is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the radio button element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "radio", name=name, checked=checked, disabled=disabled, exact=exact
            )
        )

    async def select(
        self, name: str, disabled: bool = False, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a select element (<select> or role="combobox").

        Args:
            name: Accessible name (usually from associated label)
            disabled: Whether the select is disabled
            exact: Whether to match name exactly

        Returns:
            Locator for the select element
        """
        return ElementLocator(
            self.__framework_element.get_by_role(
                "combobox", name=name, disabled=disabled, exact=exact
            )
        )

    async def image(self, name: str, exact: bool = False) -> "ElementLocator":
        """
        Locates an image element (<img> or role="img").

        Args:
            name: Alt text or accessible name of the image
            exact: Whether to match name exactly

        Returns:
            Locator for the image element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("img", name=name, exact=exact)
        )

    async def listitem(self, name: str, exact: bool = False) -> "ElementLocator":
        """
        Locates a list item element (<li> or role="listitem").

        Args:
            name: Text content of the list item
            exact: Whether to match name exactly

        Returns:
            Locator for the list item element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("listitem", name=name, exact=exact)
        )

    async def table(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a table element (<table> or role="table").

        Args:
            name: Accessible name of the table (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the table element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("table", name=name, exact=exact)
        )

    async def cell(self, name: str, exact: bool = False) -> "ElementLocator":
        """
        Locates a table cell element (<td> or role="cell").

        Args:
            name: Text content of the cell
            exact: Whether to match name exactly

        Returns:
            Locator for the table cell element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("cell", name=name, exact=exact)
        )

    async def div(
        self, name: Optional[str] = None, exact: bool = False
    ) -> "ElementLocator":
        """
        Locates a div element (generic container).

        Args:
            name: Text content or accessible name (optional)
            exact: Whether to match name exactly

        Returns:
            Locator for the div element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("generic", name=name, exact=exact)
        )

    async def paragraph(self, name: str, exact: bool = False) -> "ElementLocator":
        """
        Locates a paragraph element (<p> or role="paragraph").

        Args:
            name: Text content of the paragraph
            exact: Whether to match name exactly

        Returns:
            Locator for the paragraph element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("paragraph", name=name, exact=exact)
        )

    async def form(self, name: str, exact: bool = False) -> "ElementLocator":
        """
        Locates a form element (<form> or role="form").

        Args:
            name: Accessible name of the form
            exact: Whether to match name exactly

        Returns:
            Locator for the form element
        """
        return ElementLocator(
            self.__framework_element.get_by_role("form", name=name, exact=exact)
        )
