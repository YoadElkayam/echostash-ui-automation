"""Regression tests for the share prompt form."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.share_page import SharePage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.regression
class TestShareForm:
    """Verify share form fields and submission."""

    def test_share_form_loads(self, page: Page, base_url: str) -> None:
        """UI-SHARE-001: Share page form fields are present."""
        share = SharePage(page, base_url)
        share.open()

        name_input = page.get_by_label("Name").or_(page.get_by_placeholder("Name")).first
        content_input = page.get_by_label("Content").or_(
            page.get_by_placeholder("Paste your prompt")
        ).first
        expect(name_input).to_be_visible(timeout=5000)
        expect(content_input).to_be_visible(timeout=5000)

    def test_share_with_description(self, page: Page, base_url: str) -> None:
        """Fill name, content, and optional description."""
        share = SharePage(page, base_url)
        share.open()

        share.fill_name(unique_name("desc-share"))
        share.fill_content(random_prompt_content())
        share.fill_description("Shared with description for regression")
        share.click_share()

        assert share.is_success_visible()
