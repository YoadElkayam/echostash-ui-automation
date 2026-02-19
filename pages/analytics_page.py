"""Page object for the Analytics page."""

from __future__ import annotations

from typing import Dict, List

from playwright.sync_api import Page

from pages.base_page import BasePage


class AnalyticsPage(BasePage):
    """Analytics dashboard for prompt usage metrics."""

    PATH = "/analytics"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize AnalyticsPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the analytics page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def set_date_range(self, from_date: str, to_date: str) -> None:
        """Set the analytics date range filter.

        Args:
            from_date: Start date string (e.g. '2024-01-01').
            to_date: End date string (e.g. '2024-01-31').
        """
        from_input = self.page.locator("[data-testid='date-from']").or_(
            self.page.get_by_label("From")
        ).first
        to_input = self.page.locator("[data-testid='date-to']").or_(
            self.page.get_by_label("To")
        ).first
        self.fill_form_field(from_input, from_date)
        self.fill_form_field(to_input, to_date)
        self.wait_for_loading_complete()

    def get_overview_metrics(self) -> Dict[str, str]:
        """Get all overview metric values.

        Returns:
            Dictionary mapping metric labels to their displayed values.
        """
        self.wait_for_loading_complete()
        metrics: Dict[str, str] = {}
        cards = self.page.locator("[data-testid='metric-card']")
        for i in range(cards.count()):
            card = cards.nth(i)
            label = card.locator("[data-testid='metric-label']").inner_text()
            value = card.locator("[data-testid='metric-value']").inner_text()
            metrics[label] = value
        return metrics

    def get_top_prompts(self) -> List[str]:
        """Get the list of top prompts from the analytics view.

        Returns:
            List of prompt name strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='top-prompt-item']")
        return items.all_inner_texts()

    def select_prompt(self, name: str) -> None:
        """Select a specific prompt for detailed analytics.

        Args:
            name: Prompt name to select.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_loading_complete()
