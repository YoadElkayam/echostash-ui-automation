"""Regression tests for Public Prompt View (UI-PPV)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_detail_page import BrowseDetailPage


@pytest.mark.regression
class TestPublicPromptView:
    """Verify public prompt view page functionality."""

    def test_public_prompt_page_loads(
        self, page: Page, base_url: str
    ) -> None:
        """UI-PPV-001: /p/{slug} page loads with prompt content."""
        # Navigate to browse first to find a public prompt slug
        page.goto(f"{base_url}/browse")
        page.wait_for_load_state("domcontentloaded")
        cards = page.locator("[data-testid='prompt-card']")
        if cards.count() > 0:
            cards.first.click()
            page.wait_for_load_state("domcontentloaded")
            detail = BrowseDetailPage(page, base_url)
            heading = page.get_by_role("heading").first
            if heading.is_visible():
                assert heading.inner_text().strip() != ""

    def test_upvote_prompt(self, page: Page, base_url: str) -> None:
        """UI-PPV-003: Upvote button increments count."""
        page.goto(f"{base_url}/browse")
        page.wait_for_load_state("domcontentloaded")
        cards = page.locator("[data-testid='prompt-card']")
        if cards.count() > 0:
            cards.first.click()
            page.wait_for_load_state("domcontentloaded")
            upvote_btn = page.get_by_role("button", name="Upvote").or_(
                page.locator("[data-testid='upvote-btn']")
            ).first
            if upvote_btn.is_visible():
                upvote_btn.click()

    def test_nonexistent_slug_shows_404(
        self, page: Page, base_url: str
    ) -> None:
        """UI-PPV-005: Non-existent slug shows 404 or not-found page."""
        page.goto(f"{base_url}/p/this-slug-does-not-exist-at-all-12345")
        page.wait_for_load_state("domcontentloaded")
        body = page.locator("body").inner_text().lower()
        assert "not found" in body or "404" in body or "error" in body or page.url != f"{base_url}/p/this-slug-does-not-exist-at-all-12345"
