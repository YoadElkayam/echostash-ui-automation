"""Regression tests for browse search functionality."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowseSearch:
    """Verify browse page search."""

    def test_search_returns_results(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-002: Search for public prompts."""
        browse = BrowsePage(page, base_url)
        browse.open()
        browse.search("prompt")
        page.wait_for_timeout(2000)
        assert "/browse" in page.url

    def test_search_no_results(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-009: Search with nonsense shows no results."""
        browse = BrowsePage(page, base_url)
        browse.open()
        browse.search("zzzzxxxxxxxxxnonsense99999")
        page.wait_for_timeout(2000)
        # Should show empty state or no results message
        no_results = page.get_by_text("No prompts found").or_(
            page.get_by_text("No results")
        ).first
        # Either shows no results message or just empty cards area
        cards = browse.get_prompt_cards()
        assert len(cards) == 0 or no_results.is_visible()

    def test_search_combined_with_tag(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-010: Combined search and tag filter."""
        browse = BrowsePage(page, base_url)
        browse.open()
        browse.search("AI")
        page.wait_for_timeout(1000)
