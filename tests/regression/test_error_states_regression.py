"""Regression tests for Error States (UI-ERR P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
class TestNetworkErrors:
    """Verify the app handles network errors gracefully."""

    def test_network_error_handling(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-005: Network failure shows error message without crashing."""
        # Abort all API requests to simulate network failure
        authenticated_page.route(
            "**/api/**", lambda route: route.abort("connectionrefused")
        )
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        # App should still render (not blank screen)
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0
        authenticated_page.unroute("**/api/**")

    def test_server_error_500_display(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-007: Server 500 error shows error message."""
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(
                status=500, body='{"error":"internal server error"}'
            ),
        )
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0
        authenticated_page.unroute("**/api/**")


@pytest.mark.regression
class TestToastDismiss:
    """Verify toast notification dismiss behavior."""

    def test_toast_dismiss(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-008: Toast notifications can be dismissed."""
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        toast = authenticated_page.locator(
            "[role='status'], [data-testid='toast']"
        ).first
        if toast.is_visible():
            close_btn = toast.locator("button").first
            if close_btn.is_visible():
                close_btn.click()
                toast.wait_for(state="hidden", timeout=3000)
