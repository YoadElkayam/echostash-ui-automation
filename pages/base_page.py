"""Base page object providing common functionality for all page objects."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Base class for all page objects. Provides common UI interaction methods."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize base page.

        Args:
            page: Playwright page instance.
            base_url: Base URL for the application.
        """
        self.page = page
        self.base_url = base_url.rstrip("/")

    # ── Navigation ───────────────────────────────────────────────────────

    def navigate(self, path: str = "/") -> None:
        """Navigate to a path relative to base_url.

        Args:
            path: URL path to navigate to.
        """
        url = f"{self.base_url}{path}" if self.base_url else path
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    # ── Waiting ──────────────────────────────────────────────────────────

    def wait_for_page_load(self, timeout: int = 30000) -> None:
        """Wait for the page to be fully loaded (DOM ready + network idle).

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_for_api_response(self, url_pattern: str, timeout: int = 30000):
        """Wait for a specific API response.

        Args:
            url_pattern: URL pattern or substring to match.
            timeout: Maximum wait time in milliseconds.

        Returns:
            The matched response.
        """
        return self.page.wait_for_response(
            lambda resp: url_pattern in resp.url,
            timeout=timeout,
        )

    def wait_for_loading_complete(self, timeout: int = 10000) -> None:
        """Wait for all loading spinners and skeletons to disappear.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        for selector in [
            "[data-testid='loading']",
            ".animate-spin",
            ".skeleton",
            "[role='progressbar']",
        ]:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                locator.first.wait_for(state="hidden", timeout=timeout)

    # ── Interactions ─────────────────────────────────────────────────────

    def click_and_wait(
        self,
        locator: Locator,
        url_pattern: Optional[str] = None,
        timeout: int = 30000,
    ) -> None:
        """Click an element and optionally wait for an API response or navigation.

        Args:
            locator: Element to click.
            url_pattern: If provided, wait for a response matching this pattern.
            timeout: Maximum wait time in milliseconds.
        """
        if url_pattern:
            with self.page.expect_response(
                lambda resp: url_pattern in resp.url, timeout=timeout
            ):
                locator.click()
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

    def wait_and_click(self, locator: Locator, timeout: int = 10000) -> None:
        """Wait for an element to be visible, then click it.

        Args:
            locator: Element to click.
            timeout: Maximum wait time in milliseconds.
        """
        locator.wait_for(state="visible", timeout=timeout)
        locator.click()

    def fill_form_field(self, locator: Locator, value: str) -> None:
        """Clear a form field and fill it with a value.

        Args:
            locator: Input element to fill.
            value: Text value to enter.
        """
        locator.clear()
        locator.fill(value)

    def select_option(self, locator: Locator, value: str) -> None:
        """Select an option from a dropdown.

        Args:
            locator: Select element.
            value: Option value to select.
        """
        locator.select_option(value)

    # ── Toast / Notifications ────────────────────────────────────────────

    def get_toast_message(self, timeout: int = 5000) -> str:
        """Get the text of the currently visible toast notification.

        Args:
            timeout: Maximum wait time in milliseconds.

        Returns:
            Toast message text.
        """
        toast = self.page.locator("[role='status'], [data-testid='toast']").first
        toast.wait_for(state="visible", timeout=timeout)
        return toast.inner_text()

    def dismiss_toast(self) -> None:
        """Close the currently visible toast notification."""
        close_btn = self.page.locator(
            "[role='status'] button, [data-testid='toast'] button"
        ).first
        if close_btn.is_visible():
            close_btn.click()

    # ── Screenshots ──────────────────────────────────────────────────────

    def take_screenshot(self, name: str) -> str:
        """Take a screenshot and save it with a timestamped filename.

        Args:
            name: Base name for the screenshot file.

        Returns:
            Path to the saved screenshot.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"test-results/{name}_{timestamp}.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    # ── Element queries ──────────────────────────────────────────────────

    def is_visible(self, locator: Locator, timeout: int = 3000) -> bool:
        """Check whether an element is visible.

        Args:
            locator: Element to check.
            timeout: Maximum wait time in milliseconds.

        Returns:
            True if the element is visible within the timeout.
        """
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_text(self, locator: Locator, timeout: int = 5000) -> str:
        """Get the inner text of an element.

        Args:
            locator: Element to read.
            timeout: Maximum wait time in milliseconds.

        Returns:
            Element inner text.
        """
        locator.wait_for(state="visible", timeout=timeout)
        return locator.inner_text()

    def scroll_to(self, locator: Locator) -> None:
        """Scroll an element into the viewport.

        Args:
            locator: Element to scroll to.
        """
        locator.scroll_into_view_if_needed()

    # ── Assertions ───────────────────────────────────────────────────────

    def expect_url(self, pattern: str, timeout: int = 10000) -> None:
        """Assert the current URL matches a pattern.

        Args:
            pattern: Regex pattern to match against the URL.
            timeout: Maximum wait time in milliseconds.
        """
        expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)

    def expect_visible(self, locator: Locator, timeout: int = 10000) -> None:
        """Assert an element is visible.

        Args:
            locator: Element to assert visibility of.
            timeout: Maximum wait time in milliseconds.
        """
        expect(locator).to_be_visible(timeout=timeout)

    def expect_text(
        self, locator: Locator, text: str, timeout: int = 10000
    ) -> None:
        """Assert an element contains the given text.

        Args:
            locator: Element to check.
            text: Expected text content.
            timeout: Maximum wait time in milliseconds.
        """
        expect(locator).to_contain_text(text, timeout=timeout)

    def expect_not_visible(self, locator: Locator, timeout: int = 10000) -> None:
        """Assert an element is not visible.

        Args:
            locator: Element to assert is hidden.
            timeout: Maximum wait time in milliseconds.
        """
        expect(locator).to_be_hidden(timeout=timeout)
