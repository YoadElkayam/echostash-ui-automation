"""Page object for the Browse public prompts page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class BrowsePage(BasePage):
    """Browse page for discovering public prompts and packs."""

    PATH = "/browse"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize BrowsePage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the browse page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _search_input(self):
        """Search input."""
        return self.page.get_by_placeholder("Search")

    @property
    def _prompt_cards(self):
        """All prompt card elements."""
        return self.page.locator("[data-testid='prompt-card']")

    # ── Actions ──────────────────────────────────────────────────────────

    def search(self, query: str) -> None:
        """Search for prompts.

        Args:
            query: Search query text.
        """
        self.fill_form_field(self._search_input, query)
        self.page.keyboard.press("Enter")
        self.wait_for_loading_complete()

    def select_tab(self, tab: str) -> None:
        """Select a tab (prompts or packs).

        Args:
            tab: Tab name ('prompts' or 'packs').
        """
        self.page.get_by_role("tab", name=tab.capitalize()).or_(
            self.page.get_by_text(tab, exact=False)
        ).first.click()
        self.wait_for_loading_complete()

    def sort_by(self, option: str) -> None:
        """Sort results by a given option.

        Args:
            option: Sort option (e.g. 'newest', 'popular', 'most_viewed').
        """
        sort_btn = self.page.locator("[data-testid='sort-select']").or_(
            self.page.get_by_label("Sort")
        ).first
        sort_btn.click()
        self.page.get_by_text(option, exact=False).first.click()
        self.wait_for_loading_complete()

    def filter_by_tag(self, tag: str) -> None:
        """Filter prompts by a tag.

        Args:
            tag: Tag name to filter by.
        """
        self.page.get_by_text(tag, exact=True).first.click()
        self.wait_for_loading_complete()

    def get_prompt_cards(self) -> List[Locator]:
        """Return all visible prompt card locators.

        Returns:
            List of prompt card Locator objects.
        """
        self.wait_for_loading_complete()
        return self._prompt_cards.all()

    def click_prompt(self, name: str) -> None:
        """Click a prompt card by name.

        Args:
            name: Prompt name or text to match.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_page_load()

    def next_page(self) -> None:
        """Navigate to the next page of results."""
        self.page.get_by_role("button", name="Next").or_(
            self.page.locator("[data-testid='next-page']")
        ).first.click()
        self.wait_for_loading_complete()

    def prev_page(self) -> None:
        """Navigate to the previous page of results."""
        self.page.get_by_role("button", name="Previous").or_(
            self.page.locator("[data-testid='prev-page']")
        ).first.click()
        self.wait_for_loading_complete()

    def get_current_page(self) -> int:
        """Get the current page number.

        Returns:
            Current page number as integer.
        """
        page_indicator = self.page.locator("[data-testid='current-page']")
        if page_indicator.is_visible():
            return int(page_indicator.inner_text())
        return 1
