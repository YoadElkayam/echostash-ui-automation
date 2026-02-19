"""Page object for the API Keys settings page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class ApiKeysPage(BasePage):
    """Manage API keys for programmatic access."""

    PATH = "/api-keys"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize ApiKeysPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    def open(self) -> None:
        """Navigate to the API keys page."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Actions ──────────────────────────────────────────────────────────

    def create_key(self, name: str) -> None:
        """Create a new API key.

        Args:
            name: Name/label for the API key.
        """
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="New Key")
        ).first.click()
        name_input = self.page.get_by_label("Name").or_(
            self.page.get_by_placeholder("Key name")
        ).first
        self.fill_form_field(name_input, name)
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="Generate")
        ).first.click()
        self.wait_for_loading_complete()

    def get_key_value(self) -> str:
        """Get the displayed key value (shown once after creation).

        Returns:
            API key string.
        """
        key_el = self.page.locator("[data-testid='api-key-value'], code, input[readonly]").first
        key_el.wait_for(state="visible")
        text = key_el.inner_text()
        return text if text else key_el.input_value()

    def get_key_list(self) -> List[str]:
        """Return names of all API keys.

        Returns:
            List of key name strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='api-key-item']")
        return items.all_inner_texts()

    def revoke_key(self, name: str) -> None:
        """Revoke an API key by name.

        Args:
            name: Key name to revoke.
        """
        row = self.page.get_by_text(name, exact=False).first
        row.hover()
        self.page.get_by_role("button", name="Revoke").or_(
            self.page.get_by_role("button", name="Delete")
        ).first.click()
        # Confirm
        self.page.get_by_role("button", name="Confirm").or_(
            self.page.get_by_role("button", name="Revoke")
        ).first.click()
        self.wait_for_loading_complete()

    def is_key_visible_once_notice(self) -> bool:
        """Check if the 'key shown once' warning is visible.

        Returns:
            True if the one-time visibility notice is displayed.
        """
        notice = self.page.get_by_text("only be shown once").or_(
            self.page.get_by_text("won't be shown again")
        ).first
        return self.is_visible(notice)
