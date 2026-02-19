"""Page object for the single project view (prompt listing)."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class ProjectViewPage(BasePage):
    """View for a single project showing its prompts."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize ProjectViewPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _prompt_items(self):
        """All prompt list items within the project."""
        return self.page.locator("[data-testid='prompt-item'], [data-testid='prompt-card']")

    @property
    def _new_prompt_btn(self):
        """New prompt button."""
        return self.page.get_by_role("button", name="New Prompt").or_(
            self.page.get_by_role("button", name="Create Prompt")
        ).first

    @property
    def _search_input(self):
        """Prompt search input."""
        return self.page.get_by_placeholder("Search prompts")

    # ── Actions ──────────────────────────────────────────────────────────

    def get_prompt_list(self) -> List[str]:
        """Return the names of all prompts in the project.

        Returns:
            List of prompt name strings.
        """
        self.wait_for_loading_complete()
        return self._prompt_items.all_inner_texts()

    def click_prompt(self, name: str) -> None:
        """Click on a prompt by its name.

        Args:
            name: Prompt name to click.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_page_load()

    def click_new_prompt(self) -> None:
        """Click the new prompt button."""
        self._new_prompt_btn.click()

    def search_prompts(self, query: str) -> None:
        """Search prompts within the project.

        Args:
            query: Search query text.
        """
        self.fill_form_field(self._search_input, query)
        self.wait_for_loading_complete()

    def edit_project(self) -> None:
        """Open the edit project dialog."""
        edit_btn = self.page.get_by_role("button", name="Edit").or_(
            self.page.locator("[data-testid='edit-project']")
        ).first
        edit_btn.click()

    def delete_project(self) -> None:
        """Delete the current project (clicks delete and confirms)."""
        delete_btn = self.page.get_by_role("button", name="Delete").or_(
            self.page.locator("[data-testid='delete-project']")
        ).first
        delete_btn.click()
        # Confirm the deletion dialog
        confirm_btn = self.page.get_by_role("button", name="Confirm").or_(
            self.page.get_by_role("button", name="Delete")
        ).first
        confirm_btn.click()
        self.page.wait_for_load_state("networkidle")
