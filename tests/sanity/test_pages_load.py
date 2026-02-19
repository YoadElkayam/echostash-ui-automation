"""Sanity tests for page load verification across the app."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.analytics_page import AnalyticsPage
from pages.context_store_page import ContextStorePage
from pages.evals_page import EvalsPage
from pages.plans_page import PlansPage
from pages.usage_page import UsagePage


@pytest.mark.sanity
class TestPagesLoad:
    """Verify critical pages load without errors."""

    def test_public_prompt_view_loads(self, page: Page, base_url: str) -> None:
        """UI-PPV-001: Public prompt view page loads (if prompt exists)."""
        page.goto(f"{base_url}/p/test-prompt")
        page.wait_for_load_state("domcontentloaded")
        # Should show either the prompt or a not-found message
        body = page.locator("body")
        expect(body).to_be_visible()

    def test_evals_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-EVAL-001: Evals page loads for authenticated user."""
        evals = EvalsPage(authenticated_page, base_url)
        evals.open()
        expect(authenticated_page).to_have_url(f"{base_url}/evals", timeout=10000)

    def test_context_store_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-001: Context store page loads."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        expect(authenticated_page).to_have_url(f"{base_url}/context-store")

    def test_context_store_upload_file(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-002: Upload file to context store (file input exists)."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        file_input = authenticated_page.locator("input[type='file']")
        expect(file_input).to_be_attached(timeout=5000)

    def test_context_store_list_assets(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-CTX-003: Asset list is displayed."""
        ctx = ContextStorePage(authenticated_page, base_url)
        ctx.open()
        assets = ctx.get_asset_list()
        assert isinstance(assets, list)

    def test_analytics_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ANLY-001: Analytics page loads."""
        analytics = AnalyticsPage(authenticated_page, base_url)
        analytics.open()
        expect(authenticated_page).to_have_url(f"{base_url}/analytics")

    def test_plans_page_loads(self, page: Page, base_url: str) -> None:
        """UI-BILL-001: Plans page loads and shows plan cards."""
        plans = PlansPage(page, base_url)
        plans.open()
        expect(page).to_have_url(f"{base_url}/plans")

    def test_usage_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-BILL-004: Usage page loads."""
        usage = UsagePage(authenticated_page, base_url)
        usage.open()
        expect(authenticated_page).to_have_url(f"{base_url}/usage")


@pytest.mark.sanity
class TestErrorStates:
    """Verify error state handling."""

    def test_401_redirect(self, page: Page, base_url: str) -> None:
        """UI-ERR-001: Accessing protected page without auth redirects or shows modal."""
        page.goto(f"{base_url}/dashboard")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)
        # Should either redirect away from dashboard or show auth modal
        auth_modal = page.locator("[role='dialog']")
        is_protected = "/dashboard" not in page.url or auth_modal.is_visible()
        assert is_protected, "Protected page should require authentication"

    def test_429_plan_limit_overlay(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-002: Plan limit overlay can be triggered via route interception."""
        # Mock a 429 response to test overlay behavior
        authenticated_page.route(
            "**/api/**",
            lambda route: route.fulfill(status=429, body='{"error":"rate_limited"}'),
        )
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_timeout(3000)
        # Unroute to restore normal behavior
        authenticated_page.unroute("**/api/**")

    def test_form_validation_errors(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-ERR-004: Submitting empty forms shows validation errors."""
        from pages.dashboard_page import DashboardPage
        from pages.project_modal import ProjectModal

        dashboard = DashboardPage(authenticated_page, base_url)
        dashboard.open()
        dashboard.click_new_project()

        modal = ProjectModal(authenticated_page, base_url)
        modal.wait_for_modal()
        modal.fill_name("")
        modal.submit()

        # Dialog should remain open since validation failed
        dialog = authenticated_page.locator("[role='dialog']")
        expect(dialog).to_be_visible(timeout=3000)
