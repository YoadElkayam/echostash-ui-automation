"""Sanity tests for the share prompt page."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.share_page import SharePage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.sanity
class TestSharePrompt:
    """Verify the share prompt flow."""

    def test_share_page_loads(self, page: Page, base_url: str) -> None:
        """UI-SHARE-001: Share page loads with form fields."""
        share = SharePage(page, base_url)
        share.open()
        expect(page).to_have_url(f"{base_url}/share")

    def test_share_prompt_success(self, page: Page, base_url: str) -> None:
        """UI-SHARE-002: Fill share form and submit successfully."""
        share = SharePage(page, base_url)
        share.open()

        name = unique_name("shared-prompt")
        share.fill_name(name)
        share.fill_content(random_prompt_content())
        share.click_share()

        assert share.is_success_visible(), "Share success message should be visible"
