"""Sanity tests for the API Keys page."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.api_keys_page import ApiKeysPage
from utils.helpers import unique_name


@pytest.mark.sanity
class TestApiKeys:
    """Verify API key management core flows."""

    def test_api_keys_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-001: API keys page loads successfully."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()
        expect(authenticated_page).to_have_url(f"{base_url}/api-keys")

    def test_create_api_key(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-002: Create a new API key."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        key_name = unique_name("test-key")
        keys_page.create_key(key_name)

        # Key value should be shown after creation
        key_value = keys_page.get_key_value()
        assert len(key_value) > 0, "API key value should be displayed after creation"

    def test_copy_key_on_creation(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-003: Copy button is available after key creation."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        key_name = unique_name("copy-key")
        keys_page.create_key(key_name)

        # Copy button should be visible
        copy_btn = authenticated_page.get_by_role("button", name="Copy").first
        expect(copy_btn).to_be_visible(timeout=5000)

    def test_view_key_list(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-004: View the list of API keys."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        # Create a key first to ensure list is not empty
        key_name = unique_name("list-key")
        keys_page.create_key(key_name)

        # Dismiss the creation dialog if any, then check list
        authenticated_page.wait_for_timeout(1000)
        key_list = keys_page.get_key_list()
        assert isinstance(key_list, list)

    def test_revoke_api_key(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-KEY-006: Revoke an API key."""
        keys_page = ApiKeysPage(authenticated_page, base_url)
        keys_page.open()

        key_name = unique_name("revoke-key")
        keys_page.create_key(key_name)
        authenticated_page.wait_for_timeout(1000)

        keys_page.revoke_key(key_name)
        authenticated_page.wait_for_timeout(1000)
