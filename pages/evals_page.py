"""Page object for the Evals landing page."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class EvalsPage(BasePage):
    """Evals top-level page with prompt selection and tab navigation."""

    PATH = "/evals"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize EvalsPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the evals page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def select_prompt(self, name: str) -> None:
        """Select a prompt to evaluate.

        Args:
            name: Prompt name to select.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_loading_complete()

    def navigate_tab(self, tab_name: str) -> None:
        """Navigate to a specific eval tab.

        Args:
            tab_name: Tab name (e.g. 'Datasets', 'Suites', 'Runs', 'Results').
        """
        self.page.get_by_role("tab", name=tab_name).or_(
            self.page.get_by_text(tab_name)
        ).first.click()
        self.wait_for_loading_complete()

    def get_active_tab(self) -> str:
        """Get the name of the currently active tab.

        Returns:
            Active tab name.
        """
        active = self.page.locator("[role='tab'][aria-selected='true']")
        if active.is_visible():
            return active.inner_text()
        return ""
