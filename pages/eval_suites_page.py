"""Page object for the Eval Suites page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class EvalSuitesPage(BasePage):
    """Manage evaluation test suites."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize EvalSuitesPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Actions ──────────────────────────────────────────────────────────

    def create_suite(self, name: str) -> None:
        """Create a new evaluation suite.

        Args:
            name: Suite name.
        """
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="New Suite")
        ).first.click()
        name_input = self.page.get_by_label("Name").or_(
            self.page.get_by_placeholder("Suite name")
        ).first
        self.fill_form_field(name_input, name)
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="Save")
        ).first.click()
        self.wait_for_loading_complete()

    def get_suite_list(self) -> List[str]:
        """Return names of all suites.

        Returns:
            List of suite name strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='suite-item']")
        return items.all_inner_texts()

    def click_suite(self, name: str) -> None:
        """Click on a suite by name.

        Args:
            name: Suite name to click.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_loading_complete()

    def delete_suite(self, name: str) -> None:
        """Delete a suite by name.

        Args:
            name: Suite name to delete.
        """
        row = self.page.get_by_text(name, exact=False).first
        row.hover()
        delete_btn = self.page.get_by_role("button", name="Delete").first
        delete_btn.click()
        self.page.get_by_role("button", name="Confirm").or_(
            self.page.get_by_role("button", name="Delete")
        ).first.click()
        self.wait_for_loading_complete()
