"""Regression tests for share form validation."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.share_page import SharePage
from utils.helpers import random_prompt_content


@pytest.mark.regression
class TestShareValidation:
    """Verify share form validation."""

    def test_share_empty_name_validation(self, page: Page, base_url: str) -> None:
        """UI-SHARE-006: Empty name triggers validation error."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name("")
        share.fill_content(random_prompt_content())
        share.click_share()

        # Should not show success
        page.wait_for_timeout(2000)
        assert not share.is_success_visible()

    def test_share_empty_content_validation(self, page: Page, base_url: str) -> None:
        """UI-SHARE-007: Empty content triggers validation error."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name("Some Name")
        share.fill_content("")
        share.click_share()

        page.wait_for_timeout(2000)
        assert not share.is_success_visible()
