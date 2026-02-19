"""Reusable UI component helpers (dialogs, toasts, overlays, spinners)."""

from __future__ import annotations

from playwright.sync_api import Page


class ConfirmDialog:
    """Helper for interacting with confirmation dialogs."""

    def __init__(self, page: Page) -> None:
        """Initialize ConfirmDialog.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    @property
    def _dialog(self):
        """Dialog element."""
        return self.page.locator("[role='alertdialog'], [role='dialog']").first

    def is_visible(self) -> bool:
        """Check if a confirm dialog is visible.

        Returns:
            True if dialog is visible.
        """
        return self._dialog.is_visible()

    def confirm(self) -> None:
        """Click the confirm/OK button."""
        self._dialog.get_by_role("button", name="Confirm").or_(
            self._dialog.get_by_role("button", name="OK")
        ).or_(
            self._dialog.get_by_role("button", name="Yes")
        ).first.click()
        self._dialog.wait_for(state="hidden")

    def cancel(self) -> None:
        """Click the cancel button."""
        self._dialog.get_by_role("button", name="Cancel").or_(
            self._dialog.get_by_role("button", name="No")
        ).first.click()
        self._dialog.wait_for(state="hidden")

    def get_message(self) -> str:
        """Get the dialog message text.

        Returns:
            Dialog message string.
        """
        return self._dialog.inner_text()


class Toast:
    """Helper for interacting with toast notifications."""

    def __init__(self, page: Page) -> None:
        """Initialize Toast.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    @property
    def _toast(self):
        """Toast notification element."""
        return self.page.locator("[role='status'], [data-testid='toast']").first

    def wait_for_toast(self, timeout: int = 5000) -> None:
        """Wait for a toast notification to appear.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        self._toast.wait_for(state="visible", timeout=timeout)

    def get_message(self) -> str:
        """Get the toast message text.

        Returns:
            Toast message string.
        """
        return self._toast.inner_text()

    def dismiss(self) -> None:
        """Dismiss the toast notification."""
        close = self._toast.locator("button").first
        if close.is_visible():
            close.click()

    def is_visible(self) -> bool:
        """Check if a toast is currently visible.

        Returns:
            True if a toast is visible.
        """
        return self._toast.is_visible()


class PlanLimitOverlay:
    """Helper for the plan upgrade / limit reached overlay."""

    def __init__(self, page: Page) -> None:
        """Initialize PlanLimitOverlay.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    @property
    def _overlay(self):
        """Plan limit overlay element."""
        return self.page.locator("[data-testid='plan-limit-overlay']").or_(
            self.page.get_by_text("Upgrade", exact=False).locator("..").locator("..")
        ).first

    def is_visible(self) -> bool:
        """Check if the plan limit overlay is visible.

        Returns:
            True if overlay is displayed.
        """
        return self._overlay.is_visible()

    def click_upgrade(self) -> None:
        """Click the upgrade button on the overlay."""
        self._overlay.get_by_role("button", name="Upgrade").first.click()

    def dismiss(self) -> None:
        """Dismiss the plan limit overlay."""
        close = self._overlay.locator("button[aria-label='Close'], button:has-text('Close')").first
        if close.is_visible():
            close.click()


class LoadingSpinner:
    """Helper for detecting loading spinners."""

    def __init__(self, page: Page) -> None:
        """Initialize LoadingSpinner.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    def is_loading(self) -> bool:
        """Check if any loading spinner is visible.

        Returns:
            True if a spinner is present.
        """
        for selector in [
            "[data-testid='loading']",
            ".animate-spin",
            "[role='progressbar']",
        ]:
            if self.page.locator(selector).count() > 0:
                return True
        return False

    def wait_for_done(self, timeout: int = 10000) -> None:
        """Wait for all spinners to disappear.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        for selector in [
            "[data-testid='loading']",
            ".animate-spin",
            "[role='progressbar']",
        ]:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                locator.first.wait_for(state="hidden", timeout=timeout)
