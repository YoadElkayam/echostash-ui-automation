"""Page object for the Admin UTM Panel page."""

from __future__ import annotations

from typing import Dict, List

from playwright.sync_api import Page

from pages.base_page import BasePage


class AdminUtmPage(BasePage):
    """Admin UTM link management panel."""

    PATH = "/admin/utm-panel"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize AdminUtmPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the admin UTM panel."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def fill_utm_form(self, data: Dict[str, str]) -> None:
        """Fill the UTM link creation form.

        Args:
            data: Dictionary with form field names and values.
        """
        for field, value in data.items():
            input_el = self.page.get_by_label(field).or_(
                self.page.get_by_placeholder(field)
            ).first
            self.fill_form_field(input_el, value)

    def submit(self) -> None:
        """Submit the UTM form."""
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="Submit")
        ).first.click()
        self.wait_for_loading_complete()

    def get_link_list(self) -> List[str]:
        """Return all UTM link entries.

        Returns:
            List of UTM link text strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='utm-link-item']")
        return items.all_inner_texts()

    def delete_link(self, code: str) -> None:
        """Delete a UTM link by its code.

        Args:
            code: UTM code to delete.
        """
        row = self.page.get_by_text(code, exact=False).first
        row.hover()
        self.page.get_by_role("button", name="Delete").first.click()
        self.page.get_by_role("button", name="Confirm").or_(
            self.page.get_by_role("button", name="Delete")
        ).first.click()
        self.wait_for_loading_complete()

    def refresh_list(self) -> None:
        """Refresh the UTM link list."""
        self.page.get_by_role("button", name="Refresh").or_(
            self.page.locator("[data-testid='refresh-btn']")
        ).first.click()
        self.wait_for_loading_complete()
