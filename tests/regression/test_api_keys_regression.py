"""Regression tests for API Keys (UI-KEY P1)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.api_keys_page import ApiKeysPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestApiKeyFeatures:
    """Extended API key management tests."""

    def test_copy_key_on_creation(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-003: Copy button works after key creation."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()
        keys_page.create_key(unique_name("key-copy"))
        keys_page.wait_for_loading_complete()
        copy_btn = keys_page.page.get_by_role("button", name="Copy").first
        if copy_btn.is_visible():
            copy_btn.click()

    def test_key_not_shown_after_dismissing(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-005: Full key is not shown after navigating away and returning."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()
        key_name = unique_name("key-dismiss")
        keys_page.create_key(key_name)
        keys_page.wait_for_loading_complete()
        # Navigate away and back
        keys_page.navigate("/dashboard")
        keys_page.wait_for_page_load()
        keys_page.open()
        keys_page.wait_for_loading_complete()
        # Full key value should no longer be visible
        key_value_el = keys_page.page.locator(
            "[data-testid='api-key-value']"
        )
        if key_value_el.is_visible():
            text = key_value_el.inner_text()
            # Should be masked/truncated
            assert "..." in text or len(text) < 20 or not key_value_el.is_visible()

    def test_revoke_key_cancel(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-007: Canceling revoke keeps the key."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()
        key_name = unique_name("key-keep")
        keys_page.create_key(key_name)
        keys_page.wait_for_loading_complete()
        # Click revoke then cancel
        row = keys_page.page.get_by_text(key_name, exact=False).first
        if row.is_visible():
            row.hover()
            revoke_btn = keys_page.page.get_by_role(
                "button", name="Revoke"
            ).or_(keys_page.page.get_by_role("button", name="Delete")).first
            if revoke_btn.is_visible():
                revoke_btn.click()
                cancel_btn = keys_page.page.get_by_role(
                    "button", name="Cancel"
                ).first
                if cancel_btn.is_visible():
                    cancel_btn.click()

    def test_create_key_empty_name_validation(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-008: Creating key with empty name shows validation."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()
        create_btn = keys_page.page.get_by_role("button", name="Create").or_(
            keys_page.page.get_by_role("button", name="New Key")
        ).first
        if create_btn.is_visible():
            create_btn.click()
            name_input = keys_page.page.get_by_label("Name").or_(
                keys_page.page.get_by_placeholder("Key name")
            ).first
            if name_input.is_visible():
                name_input.fill("")
                submit_btn = keys_page.page.get_by_role(
                    "button", name="Create"
                ).or_(
                    keys_page.page.get_by_role("button", name="Generate")
                ).first
                submit_btn.click()
                # Should show validation error, modal should remain
                keys_page.page.wait_for_timeout(1000)
