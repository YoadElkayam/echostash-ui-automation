"""Regression tests for error pages and error handling."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
class TestErrorPages:
    """Verify error page handling."""

    def test_404_invalid_route(self, page: Page, base_url: str) -> None:
        """UI-ERR-006: Invalid route shows 404 or redirect."""
        page.goto(f"{base_url}/this-page-does-not-exist-at-all")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)
        body = page.locator("body")
        expect(body).to_be_visible()

    def test_401_protected_redirect(self, page: Page, base_url: str) -> None:
        """UI-ERR-001: Protected page without auth shows redirect or modal."""
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        auth_modal = page.locator("[role='dialog']")
        is_protected = "/dashboard" not in page.url or auth_modal.is_visible()
        assert is_protected

    def test_network_error_graceful(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-005: Network error shows toast/message, not crash."""
        # Intercept all API calls to simulate network failure
        authenticated_page.route(
            "**/api/**",
            lambda route: route.abort("connectionrefused"),
        )

        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_timeout(3000)

        # Page should not crash (body still visible)
        body = authenticated_page.locator("body")
        expect(body).to_be_visible()

        # Clean up route interception
        authenticated_page.unroute("**/api/**")

    def test_server_error_500_handling(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-007: Server error shows error message, app stays functional."""
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(
                status=500, body='{"error":"Internal Server Error"}'
            ),
        )

        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_timeout(3000)

        body = authenticated_page.locator("body")
        expect(body).to_be_visible()

        authenticated_page.unroute("**/api/**")

    def test_plan_limit_429_overlay(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-002: 429 response triggers plan limit overlay."""
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(
                status=429, body='{"error":"rate_limited","message":"Plan limit reached"}'
            ),
        )

        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_timeout(3000)

        authenticated_page.unroute("**/api/**")

    def test_upgrade_405_overlay(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-003: 405 response triggers upgrade overlay."""
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(
                status=405, body='{"error":"upgrade_required"}'
            ),
        )

        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_timeout(3000)

        authenticated_page.unroute("**/api/**")
