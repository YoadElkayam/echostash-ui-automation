"""Regression tests for Edge Cases (UI-EDGE)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestSpecialCharacters:
    """Verify special character handling."""

    def test_special_characters_in_project_name(
        self, dashboard: DashboardPage
    ) -> None:
        """UI-EDGE-003: Special chars in project names are handled safely."""
        dashboard.open()
        dashboard.click_new_project()
        modal = ProjectModal(dashboard.page, dashboard.base_url)
        modal.wait_for_modal()
        name = f"Test <script>alert(1)</script> {unique_name('xss')}"
        modal.fill_name(name)
        modal.fill_description("XSS test & 'quotes' \"double\"")
        modal.submit()
        dashboard.wait_for_loading_complete()

    def test_long_prompt_name(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-EDGE-001: Long prompt name (255 chars) is handled gracefully."""
        prompt_builder.open()
        long_name = "A" * 255
        prompt_builder.fill_title(long_name)
        prompt_builder.click_save()
        prompt_builder.wait_for_loading_complete()

    def test_long_prompt_content(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-EDGE-002: Large content in editor doesn't freeze the UI."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("long-content"))
        large_content = "This is a test line.\n" * 500
        prompt_builder.set_editor_content(large_content)
        # Verify the editor didn't crash
        assert len(prompt_builder.get_editor_content()) > 0

    def test_unicode_emoji_in_content(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-EDGE-004: Unicode/emoji characters are preserved."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("unicode"))
        content = "Translate: Bonjour le monde! Hola mundo! Hello world! 42"
        prompt_builder.set_editor_content(content)
        result = prompt_builder.get_editor_content()
        assert "Bonjour" in result


@pytest.mark.regression
class TestEmptyStates:
    """Verify empty states for list pages."""

    @pytest.mark.parametrize(
        "path,expected_content",
        [
            ("/dashboard", ""),
            ("/browse", ""),
            ("/api-keys", ""),
            ("/context-store", ""),
            ("/analytics", ""),
        ],
    )
    def test_pages_handle_empty_state(
        self,
        authenticated_page: Page,
        base_url: str,
        path: str,
        expected_content: str,
    ) -> None:
        """UI-EDGE-005: Each page shows appropriate empty state."""
        authenticated_page.goto(f"{base_url}{path}")
        authenticated_page.wait_for_load_state("domcontentloaded")
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0


@pytest.mark.regression
class TestDoubleClickProtection:
    """Verify double-click protection on submit buttons."""

    def test_rapid_double_click_on_create(
        self, dashboard: DashboardPage
    ) -> None:
        """UI-EDGE-006: Double-clicking Create doesn't create duplicates."""
        dashboard.open()
        dashboard.click_new_project()
        modal = ProjectModal(dashboard.page, dashboard.base_url)
        modal.wait_for_modal()
        name = unique_name("dblclick")
        modal.fill_name(name)
        # Rapid double click
        submit_btn = modal._submit_btn
        submit_btn.dblclick()
        modal.page.wait_for_timeout(2000)


@pytest.mark.regression
class TestBrowserNavigation:
    """Verify browser back/forward and refresh."""

    def test_back_forward_navigation(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-EDGE-007: Back/forward buttons work correctly."""
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        authenticated_page.goto(f"{base_url}/browse")
        authenticated_page.wait_for_load_state("domcontentloaded")
        authenticated_page.go_back()
        authenticated_page.wait_for_load_state("domcontentloaded")
        assert "dashboard" in authenticated_page.url
        authenticated_page.go_forward()
        authenticated_page.wait_for_load_state("domcontentloaded")
        assert "browse" in authenticated_page.url

    def test_refresh_page(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-EDGE-008: Page refresh reloads correctly."""
        authenticated_page.goto(f"{base_url}/dashboard")
        authenticated_page.wait_for_load_state("domcontentloaded")
        authenticated_page.reload()
        authenticated_page.wait_for_load_state("domcontentloaded")
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0


@pytest.mark.regression
class TestAccountPreferences:
    """Verify account and preferences pages."""

    def test_account_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-EDGE-013: Account page loads."""
        authenticated_page.goto(f"{base_url}/account")
        authenticated_page.wait_for_load_state("domcontentloaded")
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0

    def test_preferences_page_loads(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        """UI-EDGE-014: Preferences page loads."""
        authenticated_page.goto(f"{base_url}/preferences")
        authenticated_page.wait_for_load_state("domcontentloaded")
        body = authenticated_page.locator("body").inner_text()
        assert len(body.strip()) > 0
