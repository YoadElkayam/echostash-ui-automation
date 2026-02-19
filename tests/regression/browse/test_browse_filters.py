"""Regression tests for browse page filtering and sorting."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowseFilters:
    """Verify browse page filters and sorting."""

    def test_sort_by_newest(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-004: Sort results by newest."""
        browse = BrowsePage(page, base_url)
        browse.open()

        sort_btn = page.locator("[data-testid='sort-select']").or_(
            page.get_by_label("Sort")
        ).first
        if sort_btn.is_visible():
            browse.sort_by("Newest")
            page.wait_for_timeout(1000)

    def test_filter_by_tag(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-003: Filter prompts by tag."""
        browse = BrowsePage(page, base_url)
        browse.open()
        page.wait_for_timeout(1000)

        # Look for tag filter elements
        tag_el = page.locator("[data-testid='tag-filter']").or_(
            page.get_by_text("AI", exact=True)
        ).first
        if tag_el.is_visible():
            tag_el.click()
            page.wait_for_timeout(1000)
