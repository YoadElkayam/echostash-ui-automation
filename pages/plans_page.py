"""Page object for the Plans page."""

from __future__ import annotations

from typing import Dict, List

from playwright.sync_api import Page

from pages.base_page import BasePage


class PlansPage(BasePage):
    """Plans page showing available subscription plans."""

    PATH = "/plans"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize PlansPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the plans page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def get_plan_list(self) -> List[str]:
        """Return the names of all available plans.

        Returns:
            List of plan name strings.
        """
        self.wait_for_loading_complete()
        cards = self.page.locator("[data-testid='plan-card']")
        return cards.all_inner_texts()

    def get_plan_details(self, name: str) -> Dict[str, str]:
        """Get details of a specific plan.

        Args:
            name: Plan name to get details for.

        Returns:
            Dictionary with plan detail fields.
        """
        card = self.page.get_by_text(name, exact=False).first.locator("..")
        details: Dict[str, str] = {}
        price = card.locator("[data-testid='plan-price']")
        if price.is_visible():
            details["price"] = price.inner_text()
        features = card.locator("[data-testid='plan-features']")
        if features.is_visible():
            details["features"] = features.inner_text()
        return details
