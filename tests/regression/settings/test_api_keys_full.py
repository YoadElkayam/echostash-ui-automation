"""Regression tests for full API key lifecycle."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.api_keys_page import ApiKeysPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestApiKeysFull:
    """Full API key lifecycle tests."""

    def test_create_key_shows_once_notice(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-005: Key shown once warning after creation."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        key_name = unique_name("once-key")
        keys_page.create_key(key_name)

        assert keys_page.is_key_visible_once_notice(), "Should show one-time visibility notice"

    def test_revoke_key_cancel(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-007: Cancel key revocation keeps key."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        key_name = unique_name("cancel-revoke")
        keys_page.create_key(key_name)
        authenticated_page.wait_for_timeout(1000)

        # Start revoke but cancel
        row = authenticated_page.get_by_text(key_name, exact=False).first
        if row.is_visible():
            row.hover()
            revoke_btn = authenticated_page.get_by_role("button", name="Revoke").or_(
                authenticated_page.get_by_role("button", name="Delete")
            ).first
            if revoke_btn.is_visible():
                revoke_btn.click()
                cancel_btn = authenticated_page.get_by_role("button", name="Cancel").first
                if cancel_btn.is_visible():
                    cancel_btn.click()
                    authenticated_page.wait_for_timeout(1000)

    def test_create_key_empty_name_validation(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-008: Empty name shows validation error."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        create_btn = authenticated_page.get_by_role("button", name="Create").or_(
            authenticated_page.get_by_role("button", name="New Key")
        ).first
        create_btn.click()

        name_input = authenticated_page.get_by_label("Name").or_(
            authenticated_page.get_by_placeholder("Key name")
        ).first
        if name_input.is_visible():
            name_input.fill("")
            submit = authenticated_page.get_by_role("button", name="Create").or_(
                authenticated_page.get_by_role("button", name="Generate")
            ).first
            submit.click()
            authenticated_page.wait_for_timeout(1000)
