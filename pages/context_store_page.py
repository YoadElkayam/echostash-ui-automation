"""Page object for the Context Store page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class ContextStorePage(BasePage):
    """Manage context store assets (uploaded files for prompt context)."""

    PATH = "/context-store"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize ContextStorePage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the context store page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def upload_file(self, path: str, asset_id: str = "") -> None:
        """Upload a file to the context store.

        Args:
            path: Local file path to upload.
            asset_id: Optional asset ID / label.
        """
        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(path)
        if asset_id:
            id_input = self.page.get_by_label("Asset ID").or_(
                self.page.get_by_placeholder("Asset ID")
            ).first
            self.fill_form_field(id_input, asset_id)
        self.wait_for_loading_complete()

    def get_asset_list(self) -> List[str]:
        """Return names/IDs of all stored assets.

        Returns:
            List of asset identifier strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='asset-item']")
        return items.all_inner_texts()

    def view_asset(self, asset_id: str) -> None:
        """View a specific asset.

        Args:
            asset_id: Asset identifier to view.
        """
        self.page.get_by_text(asset_id, exact=False).first.click()
        self.wait_for_loading_complete()

    def delete_asset(self, asset_id: str) -> None:
        """Delete a specific asset.

        Args:
            asset_id: Asset identifier to delete.
        """
        row = self.page.get_by_text(asset_id, exact=False).first
        row.hover()
        self.page.get_by_role("button", name="Delete").first.click()
        self.page.get_by_role("button", name="Confirm").or_(
            self.page.get_by_role("button", name="Delete")
        ).first.click()
        self.wait_for_loading_complete()

    def get_usage(self) -> str:
        """Get the current storage usage text.

        Returns:
            Usage text (e.g. '2.5 MB / 10 MB').
        """
        usage_el = self.page.locator("[data-testid='storage-usage']")
        if usage_el.is_visible():
            return usage_el.inner_text()
        return ""
