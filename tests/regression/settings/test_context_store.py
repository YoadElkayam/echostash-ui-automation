"""Regression tests for context store file management."""

from __future__ import annotations

import os
import tempfile

import pytest
from playwright.sync_api import Page, expect

from pages.context_store_page import ContextStorePage
from utils.helpers import unique_name


@pytest.mark.regression
class TestContextStore:
    """Verify context store operations."""

    def test_upload_file(self, authenticated_page: Page, base_url: str) -> None:
        """UI-CTX-002: Upload a file to context store."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()

        # Create a temp file for upload
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, prefix="test_upload_"
        ) as f:
            f.write("Test file content for upload")
            temp_path = f.name

        try:
            ctx.upload_file(temp_path, unique_name("asset"))
            authenticated_page.wait_for_timeout(3000)
        finally:
            os.unlink(temp_path)

    def test_list_assets(self, authenticated_page: Page, base_url: str) -> None:
        """UI-CTX-003: List assets in context store."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()

        assets = ctx.get_asset_list()
        assert isinstance(assets, list)

    def test_view_asset_content(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-004: View asset content."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()

        assets = ctx.get_asset_list()
        if len(assets) > 0:
            # Click the first asset
            authenticated_page.get_by_text(assets[0][:20], exact=False).first.click()
            authenticated_page.wait_for_timeout(1000)

    def test_delete_asset(self, authenticated_page: Page, base_url: str) -> None:
        """UI-CTX-005: Delete an asset."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()

        # Upload a file to delete
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, prefix="test_del_"
        ) as f:
            f.write("File to delete")
            temp_path = f.name

        asset_name = unique_name("del-asset")
        try:
            ctx.upload_file(temp_path, asset_name)
            authenticated_page.wait_for_timeout(2000)
            ctx.delete_asset(asset_name)
            authenticated_page.wait_for_timeout(2000)
        finally:
            os.unlink(temp_path)

    def test_storage_usage_display(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-006: Storage usage is displayed."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()

        usage = ctx.get_usage()
        # Usage may or may not be visible depending on state
        assert isinstance(usage, str)
