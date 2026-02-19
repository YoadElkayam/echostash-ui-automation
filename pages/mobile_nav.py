"""Page object for mobile navigation (hamburger menu)."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class MobileNav(BasePage):
    """Mobile navigation menu for responsive layouts."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize MobileNav.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _menu_btn(self):
        """Hamburger menu button."""
        return self.page.get_by_role("button", name="Menu").or_(
            self.page.locator("[data-testid='mobile-menu-btn']")
        ).first

    @property
    def _close_btn(self):
        """Close menu button."""
        return self.page.get_by_role("button", name="Close").or_(
            self.page.locator("[data-testid='mobile-menu-close']")
        ).first

    @property
    def _menu_panel(self):
        """Mobile menu panel."""
        return self.page.locator("[data-testid='mobile-menu'], [role='dialog']").first

    # ── Actions ──────────────────────────────────────────────────────────

    def open_menu(self) -> None:
        """Open the mobile navigation menu."""
        self._menu_btn.click()
        self._menu_panel.wait_for(state="visible")

    def close_menu(self) -> None:
        """Close the mobile navigation menu."""
        self._close_btn.click()
        self._menu_panel.wait_for(state="hidden")

    def navigate_to(self, page_name: str) -> None:
        """Navigate to a page using the mobile menu.

        Args:
            page_name: Display name of the page to navigate to.
        """
        if not self._menu_panel.is_visible():
            self.open_menu()
        self._menu_panel.get_by_text(page_name, exact=False).first.click()
        self.wait_for_page_load()
