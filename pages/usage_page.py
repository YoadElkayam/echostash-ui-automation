"""Page object for the Usage page."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class UsagePage(BasePage):
    """Usage page showing quota and spending information."""

    PATH = "/usage"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize UsagePage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the usage page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def get_quota_usage(self) -> str:
        """Get the current quota usage text.

        Returns:
            Quota usage string (e.g. '150 / 1000 requests').
        """
        self.wait_for_loading_complete()
        usage_el = self.page.locator("[data-testid='quota-usage']").or_(
            self.page.get_by_text("requests", exact=False)
        ).first
        return self.get_text(usage_el)

    def get_spending_info(self) -> str:
        """Get the current spending information text.

        Returns:
            Spending info string.
        """
        self.wait_for_loading_complete()
        spending_el = self.page.locator("[data-testid='spending-info']").or_(
            self.page.get_by_text("spending", exact=False)
        ).first
        return self.get_text(spending_el)
