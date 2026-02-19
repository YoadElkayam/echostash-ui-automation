"""Page object for authentication flows (guest login, Google OAuth, logout)."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class AuthPage(BasePage):
    """Handles guest login, Google login, auth modal, and logout."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize AuthPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _auth_modal(self):
        """Auth modal dialog."""
        return self.page.locator("[role='dialog']")

    @property
    def _guest_login_btn(self):
        """Guest login button."""
        return self.page.get_by_role("button", name="Guest")

    @property
    def _google_login_btn(self):
        """Google login button."""
        return self.page.get_by_role("button", name="Google")

    @property
    def _close_modal_btn(self):
        """Close modal button."""
        return self._auth_modal.locator("button[aria-label='Close'], button:has-text('Close'), button:has-text('x')").first

    # ── Actions ──────────────────────────────────────────────────────────

    def wait_for_auth_modal(self, timeout: int = 10000) -> None:
        """Wait for the auth modal to appear.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        self._auth_modal.wait_for(state="visible", timeout=timeout)

    def close_auth_modal(self) -> None:
        """Close the auth modal if visible."""
        if self._auth_modal.is_visible():
            self._close_modal_btn.click()
            self._auth_modal.wait_for(state="hidden")

    def click_guest_login(self) -> None:
        """Click the guest login button and wait for navigation."""
        self._guest_login_btn.click()
        self.page.wait_for_load_state("networkidle")

    def click_google_login(self) -> None:
        """Click the Google login button."""
        self._google_login_btn.click()

    def is_logged_in(self) -> bool:
        """Check whether the user is currently logged in.

        Returns:
            True if the user appears to be authenticated.
        """
        # Check for the presence of dashboard link or user avatar
        dashboard_link = self.page.get_by_role("link", name="Dashboard")
        user_menu = self.page.locator("[data-testid='user-menu'], [data-testid='avatar']")
        return dashboard_link.is_visible() or user_menu.is_visible()

    def logout(self) -> None:
        """Sign out the current user."""
        user_menu = self.page.locator("[data-testid='user-menu'], [data-testid='avatar']").first
        if user_menu.is_visible():
            user_menu.click()
        sign_out_btn = self.page.get_by_role("menuitem", name="Sign out").or_(
            self.page.get_by_text("Sign out")
        )
        sign_out_btn.first.click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_protected_page(self, path: str) -> None:
        """Navigate to a protected page (should trigger auth modal).

        Args:
            path: Protected route path (e.g. /dashboard).
        """
        self.navigate(path)
