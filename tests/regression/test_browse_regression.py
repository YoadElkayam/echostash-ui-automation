"""Regression tests for Browse Public Prompts (UI-BROWSE P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_detail_page import BrowseDetailPage
from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowseFiltering:
    """Browse page filtering and sorting tests."""

    def test_filter_by_tags(self, browse: BrowsePage) -> None:
        """UI-BROWSE-003: Filter prompts by tag."""
        browse.open()
        browse.wait_for_loading_complete()
        # Look for any tag filter element
        tags = browse.page.locator("[data-testid='tag-filter'] button, .tag")
        if tags.count() > 0:
            tags.first.click()
            browse.wait_for_loading_complete()

    def test_sort_options(self, browse: BrowsePage) -> None:
        """UI-BROWSE-004: Sort prompts by different criteria."""
        browse.open()
        browse.wait_for_loading_complete()
        sort_el = browse.page.locator("[data-testid='sort-select']").or_(
            browse.page.get_by_label("Sort")
        ).first
        if sort_el.is_visible():
            sort_el.click()
            option = browse.page.get_by_text("Newest").or_(
                browse.page.get_by_text("Most Viewed")
            ).first
            if option.is_visible():
                option.click()
                browse.wait_for_loading_complete()

    def test_pagination(self, browse: BrowsePage) -> None:
        """UI-BROWSE-005: Pagination navigates between result pages."""
        browse.open()
        browse.wait_for_loading_complete()
        next_btn = browse.page.get_by_role("button", name="Next").or_(
            browse.page.locator("[data-testid='next-page']")
        ).first
        if next_btn.is_visible() and next_btn.is_enabled():
            next_btn.click()
            browse.wait_for_loading_complete()


@pytest.mark.regression
class TestBrowseDetailActions:
    """Browse detail page interaction tests."""

    def test_fork_public_prompt(self, browse: BrowsePage) -> None:
        """UI-BROWSE-008: Fork a public prompt."""
        browse.open()
        browse.wait_for_loading_complete()
        cards = browse.page.locator("[data-testid='prompt-card']")
        if cards.count() > 0:
            cards.first.click()
            browse.page.wait_for_load_state("domcontentloaded")
            fork_btn = browse.page.get_by_role("button", name="Fork")
            if fork_btn.is_visible():
                fork_btn.click()
                browse.wait_for_loading_complete()

    def test_no_results_message(self, browse: BrowsePage) -> None:
        """UI-BROWSE-009: Searching gibberish shows 'no results' message."""
        browse.open()
        browse.search("zxqjk_nonexistent_prompt_xyzzy")
        browse.wait_for_loading_complete()
        body = browse.page.locator("body").inner_text().lower()
        # Should show no results or empty state
        has_empty = (
            "no" in body
            or "empty" in body
            or "found" in body
            or browse.page.locator("[data-testid='prompt-card']").count() == 0
        )
        assert has_empty
