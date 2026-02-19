"""Page object for the main dashboard view."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page with project list and semantic search."""

    PATH = "/dashboard"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize DashboardPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the dashboard."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _project_cards(self):
        """All project card elements."""
        return self.page.locator("[data-testid='project-card']")

    @property
    def _search_input(self):
        """Semantic search input."""
        return self.page.get_by_placeholder("Search")

    @property
    def _new_project_btn(self):
        """New project button."""
        return self.page.get_by_role("button", name="New Project").or_(
            self.page.get_by_role("button", name="Create Project")
        ).first

    # ── Actions ──────────────────────────────────────────────────────────

    def get_project_count(self) -> int:
        """Return the number of project cards visible on the dashboard.

        Returns:
            Count of project cards.
        """
        self.wait_for_loading_complete()
        return self._project_cards.count()

    def get_prompt_count(self) -> int:
        """Return the total prompt count displayed on the dashboard.

        Returns:
            Prompt count as integer.
        """
        counter = self.page.locator("[data-testid='prompt-count']")
        if counter.is_visible():
            return int(counter.inner_text())
        return 0

    def search_semantic(self, query: str) -> None:
        """Perform a semantic search on the dashboard.

        Args:
            query: Search query text.
        """
        self.fill_form_field(self._search_input, query)
        self.page.keyboard.press("Enter")
        self.wait_for_loading_complete()

    def click_new_project(self) -> None:
        """Click the button to create a new project."""
        self._new_project_btn.click()

    def get_project_list(self) -> List[str]:
        """Return the names of all visible projects.

        Returns:
            List of project name strings.
        """
        self.wait_for_loading_complete()
        return self._project_cards.all_inner_texts()

    def click_project(self, name: str) -> None:
        """Click a project card by name.

        Args:
            name: Project name to click.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_page_load()

    def open_share_prompt(self) -> None:
        """Open the share prompt dialog from the dashboard."""
        share_btn = self.page.get_by_role("button", name="Share").or_(
            self.page.get_by_text("Share a prompt")
        ).first
        share_btn.click()
