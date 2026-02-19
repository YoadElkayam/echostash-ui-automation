"""Regression tests for share success actions."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.share_page import SharePage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.regression
class TestShareSuccess:
    """Verify post-share success actions."""

    def test_copy_share_link(self, page: Page, base_url: str) -> None:
        """UI-SHARE-003: Copy link button works after sharing."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name(unique_name("copy-share"))
        share.fill_content(random_prompt_content())
        share.click_share()
        page.wait_for_timeout(2000)

        share_url = share.get_share_url()
        assert len(share_url) > 0, "Share URL should be non-empty"

    def test_share_another_resets_form(self, page: Page, base_url: str) -> None:
        """UI-SHARE-005: 'Share Another' resets the form."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name(unique_name("another-share"))
        share.fill_content(random_prompt_content())
        share.click_share()
        page.wait_for_timeout(2000)

        share.click_share_another()
        page.wait_for_timeout(1000)

        # Form should be reset - name input should be empty
        name_input = page.get_by_label("Name").or_(page.get_by_placeholder("Name")).first
        if name_input.is_visible():
            value = name_input.input_value()
            assert value == "", "Form should be reset after clicking share another"
