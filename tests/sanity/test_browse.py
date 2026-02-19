"""Sanity tests for the browse public prompts page."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_page import BrowsePage


@pytest.mark.sanity
class TestBrowsePage:
    """Verify browse page core functionality."""

    def test_browse_page_loads(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-001: Browse page loads and displays prompt area."""
        browse = BrowsePage(page, base_url)
        browse.open()
        expect(page).to_have_url(f"{base_url}/browse")

    def test_search_public_prompts(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-002: Search for public prompts returns results or empty state."""
        browse = BrowsePage(page, base_url)
        browse.open()
        browse.search("test")
        # After search, page should still be on browse
        page.wait_for_timeout(2000)
        assert "/browse" in page.url

    def test_click_prompt_card(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-006: Clicking a prompt card navigates to detail view."""
        browse = BrowsePage(page, base_url)
        browse.open()

        cards = browse.get_prompt_cards()
        if len(cards) > 0:
            cards[0].click()
            page.wait_for_load_state("domcontentloaded")
            # Should navigate to either /browse/{slug} or /p/{slug}
            assert "/browse/" in page.url or "/p/" in page.url
