"""Page object for the browse prompt detail page."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class BrowseDetailPage(BasePage):
    """Detail view for a single public prompt."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize BrowseDetailPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Actions ──────────────────────────────────────────────────────────

    def get_prompt_name(self) -> str:
        """Get the prompt title/name.

        Returns:
            Prompt name string.
        """
        heading = self.page.get_by_role("heading").first
        return self.get_text(heading)

    def get_prompt_content(self) -> str:
        """Get the prompt content text.

        Returns:
            Prompt content string.
        """
        content = self.page.locator("[data-testid='prompt-content']").or_(
            self.page.locator("pre, code")
        ).first
        return self.get_text(content)

    def click_fork(self) -> None:
        """Click the Fork button to fork the prompt."""
        self.page.get_by_role("button", name="Fork").click()
        self.wait_for_loading_complete()

    def click_upvote(self) -> None:
        """Click the upvote button."""
        self.page.get_by_role("button", name="Upvote").or_(
            self.page.locator("[data-testid='upvote-btn']")
        ).first.click()

    def get_view_count(self) -> int:
        """Get the view count for the prompt.

        Returns:
            View count as integer.
        """
        views_el = self.page.locator("[data-testid='view-count']")
        if views_el.is_visible():
            text = views_el.inner_text().replace(",", "")
            return int("".join(filter(str.isdigit, text)) or "0")
        return 0

    def get_upvote_count(self) -> int:
        """Get the upvote count for the prompt.

        Returns:
            Upvote count as integer.
        """
        upvote_el = self.page.locator("[data-testid='upvote-count']")
        if upvote_el.is_visible():
            text = upvote_el.inner_text().replace(",", "")
            return int("".join(filter(str.isdigit, text)) or "0")
        return 0
