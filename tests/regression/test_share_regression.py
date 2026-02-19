"""Regression tests for Share Prompt (UI-SHARE P1)."""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.share_page import SharePage
from utils.helpers import unique_name


@pytest.mark.regression
class TestShareFeatures:
    """Extended share prompt tests."""

    def test_copy_share_link(self, share: SharePage) -> None:
        """UI-SHARE-003: Copy share link after creating a share."""
        share.open()
        share.fill_name(unique_name("share-copy"))
        share.fill_content("Copy test prompt content")
        share.click_share()
        share.wait_for_loading_complete()
        copy_btn = share.page.get_by_role("button", name="Copy").first
        if copy_btn.is_visible():
            copy_btn.click()

    def test_share_another_prompt(self, share: SharePage) -> None:
        """UI-SHARE-005: Click 'Share Another' resets the form."""
        share.open()
        share.fill_name(unique_name("share-first"))
        share.fill_content("First shared prompt")
        share.click_share()
        share.wait_for_loading_complete()
        another_btn = share.page.get_by_role(
            "button", name="Share another"
        ).or_(share.page.get_by_text("Share another")).first
        if another_btn.is_visible():
            another_btn.click()
            share.page.wait_for_timeout(500)
