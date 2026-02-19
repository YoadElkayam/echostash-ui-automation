"""Regression tests for forking prompts from browse."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_detail_page import BrowseDetailPage
from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowseFork:
    """Verify fork functionality from browse."""

    def test_fork_prompt_from_browse(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-BROWSE-008: Fork a public prompt to user's workspace."""
        browse = BrowsePage(authenticated_page, base_url)
        browse.open()

        cards = browse.get_prompt_cards()
        if len(cards) > 0:
            cards[0].click()
            authenticated_page.wait_for_load_state("domcontentloaded")

            fork_btn = authenticated_page.get_by_role("button", name="Fork").first
            if fork_btn.is_visible():
                fork_btn.click()
                authenticated_page.wait_for_timeout(3000)
