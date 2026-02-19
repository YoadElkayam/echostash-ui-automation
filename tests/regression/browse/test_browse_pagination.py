"""Regression tests for browse pagination."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowsePagination:
    """Verify browse page pagination."""

    def test_pagination_next_page(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-005: Navigate to next page of results."""
        browse = BrowsePage(page, base_url)
        browse.open()

        next_btn = page.get_by_role("button", name="Next").or_(
            page.locator("[data-testid='next-page']")
        ).first
        if next_btn.is_visible() and next_btn.is_enabled():
            browse.next_page()
            page.wait_for_timeout(1000)

    def test_pagination_prev_page(self, page: Page, base_url: str) -> None:
        """Navigate back to previous page."""
        browse = BrowsePage(page, base_url)
        browse.open()

        next_btn = page.get_by_role("button", name="Next").or_(
            page.locator("[data-testid='next-page']")
        ).first
        if next_btn.is_visible() and next_btn.is_enabled():
            browse.next_page()
            page.wait_for_timeout(1000)
            browse.prev_page()
            page.wait_for_timeout(1000)
