"""Page object for the Share prompt page."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class SharePage(BasePage):
    """Share page for quickly sharing prompt content."""

    PATH = "/share"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize SharePage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the share page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _name_input(self):
        """Name input field."""
        return self.page.get_by_label("Name").or_(
            self.page.get_by_placeholder("Name")
        ).first

    @property
    def _content_input(self):
        """Content textarea."""
        return self.page.get_by_label("Content").or_(
            self.page.get_by_placeholder("Paste your prompt")
        ).first

    @property
    def _description_input(self):
        """Description input."""
        return self.page.get_by_label("Description").or_(
            self.page.get_by_placeholder("Description")
        ).first

    @property
    def _share_btn(self):
        """Share button."""
        return self.page.get_by_role("button", name="Share")

    @property
    def _copy_btn(self):
        """Copy link button."""
        return self.page.get_by_role("button", name="Copy")

    # ── Actions ──────────────────────────────────────────────────────────

    def fill_name(self, name: str) -> None:
        """Fill the share name field.

        Args:
            name: Name for the shared prompt.
        """
        self.fill_form_field(self._name_input, name)

    def fill_content(self, content: str) -> None:
        """Fill the share content field.

        Args:
            content: Prompt content to share.
        """
        self.fill_form_field(self._content_input, content)

    def fill_description(self, description: str) -> None:
        """Fill the share description field.

        Args:
            description: Description text.
        """
        self.fill_form_field(self._description_input, description)

    def click_share(self) -> None:
        """Click the Share button."""
        self._share_btn.click()
        self.wait_for_loading_complete()

    def get_share_url(self) -> str:
        """Get the generated share URL after sharing.

        Returns:
            The share URL string.
        """
        url_el = self.page.locator("[data-testid='share-url'], input[readonly]").first
        url_el.wait_for(state="visible")
        return url_el.input_value()

    def click_copy(self) -> None:
        """Click the copy link button."""
        self._copy_btn.click()

    def is_success_visible(self) -> bool:
        """Check if the success message is visible.

        Returns:
            True if success indicator is displayed.
        """
        success = self.page.get_by_text("Success").or_(
            self.page.get_by_text("Shared")
        ).first
        return self.is_visible(success)

    def click_share_another(self) -> None:
        """Click the 'Share another' button to reset the form."""
        btn = self.page.get_by_role("button", name="Share another").or_(
            self.page.get_by_text("Share another")
        ).first
        btn.click()
