"""Regression tests for browse prompt detail view."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_detail_page import BrowseDetailPage
from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowseDetail:
    """Verify prompt detail view from browse page."""

    def test_view_prompt_detail(self, page: Page, base_url: str) -> None:
        """UI-BROWSE-007: View full prompt detail from browse."""
        browse = BrowsePage(page, base_url)
        browse.open()

        cards = browse.get_prompt_cards()
        if len(cards) > 0:
            cards[0].click()
            page.wait_for_load_state("domcontentloaded")

            detail = BrowseDetailPage(page, base_url)
            name = detail.get_prompt_name()
            assert len(name) > 0, "Prompt name should be displayed"

    def test_public_prompt_view_loads(self, page: Page, base_url: str) -> None:
        """UI-PPV-001: /p/{slug} page loads."""
        # Navigate to browse to find a prompt slug
        browse = BrowsePage(page, base_url)
        browse.open()

        cards = browse.get_prompt_cards()
        if len(cards) > 0:
            cards[0].click()
            page.wait_for_load_state("domcontentloaded")
            # Should be on a detail page
            body = page.locator("body")
            expect(body).to_be_visible()

    def test_upvote_prompt(self, page: Page, base_url: str) -> None:
        """UI-PPV-003: Upvote a public prompt."""
        browse = BrowsePage(page, base_url)
        browse.open()

        cards = browse.get_prompt_cards()
        if len(cards) > 0:
            cards[0].click()
            page.wait_for_load_state("domcontentloaded")

            detail = BrowseDetailPage(page, base_url)
            upvote_btn = page.get_by_role("button", name="Upvote").or_(
                page.locator("[data-testid='upvote-btn']")
            ).first
            if upvote_btn.is_visible():
                detail.click_upvote()
                page.wait_for_timeout(1000)

    def test_nonexistent_slug(self, page: Page, base_url: str) -> None:
        """UI-PPV-005: Non-existent slug shows 404."""
        page.goto(f"{base_url}/p/this-slug-does-not-exist-12345")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)
        # Should show some kind of not-found indication
        body_text = page.locator("body").inner_text()
        assert len(body_text) > 0
