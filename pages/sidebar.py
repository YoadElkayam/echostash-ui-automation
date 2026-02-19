"""Page object for the application sidebar navigation."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class Sidebar(BasePage):
    """Sidebar navigation component."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize Sidebar.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _sidebar(self):
        """Sidebar container."""
        return self.page.locator("nav, aside, [data-testid='sidebar']").first

    @property
    def _user_menu(self):
        """User menu trigger."""
        return self.page.locator("[data-testid='user-menu'], [data-testid='avatar']").first

    # ── Actions ──────────────────────────────────────────────────────────

    def navigate_to(self, page_name: str) -> None:
        """Navigate to a page using the sidebar.

        Args:
            page_name: Display name of the page to navigate to.
        """
        link = self._sidebar.get_by_text(page_name, exact=False).first
        link.click()
        self.wait_for_page_load()

    def get_active_page(self) -> str:
        """Get the name of the currently active sidebar item.

        Returns:
            Active page name string.
        """
        active = self._sidebar.locator("[aria-current='page'], .active, [data-active='true']").first
        if active.is_visible():
            return active.inner_text()
        return ""

    def get_user_name(self) -> str:
        """Get the displayed user name from the sidebar.

        Returns:
            User name string.
        """
        name_el = self.page.locator("[data-testid='user-name']")
        if name_el.is_visible():
            return name_el.inner_text()
        return ""

    def get_user_email(self) -> str:
        """Get the displayed user email from the sidebar.

        Returns:
            User email string.
        """
        email_el = self.page.locator("[data-testid='user-email']")
        if email_el.is_visible():
            return email_el.inner_text()
        return ""

    def open_user_menu(self) -> None:
        """Open the user dropdown menu."""
        self._user_menu.click()

    def click_sign_out(self) -> None:
        """Click the sign-out option from the user menu."""
        self.open_user_menu()
        self.page.get_by_role("menuitem", name="Sign out").or_(
            self.page.get_by_text("Sign out")
        ).first.click()
        self.page.wait_for_load_state("networkidle")
