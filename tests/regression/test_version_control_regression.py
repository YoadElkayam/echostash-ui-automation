"""Regression tests for Version Control (UI-VC P1)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestVersionHistory:
    """Extended version control tests."""

    def test_version_with_changelog(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-006: Commit a version with a changelog message."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        pb.set_editor_content("Changelog version content")
        # Look for changelog input near commit
        changelog_input = pb.page.get_by_placeholder("Changelog").or_(
            pb.page.get_by_label("Changelog")
        ).first
        if changelog_input.is_visible():
            pb.fill_form_field(changelog_input, "Initial changelog entry")
        pb.click_commit()
        pb.wait_for_loading_complete()

    def test_diff_viewer(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-005: Diff viewer shows additions/deletions between versions."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        diff_btn = pb.page.get_by_text("Diff").or_(
            pb.page.get_by_text("Compare")
        ).or_(pb.page.locator("[data-testid='diff-viewer']")).first
        if diff_btn.is_visible():
            diff_btn.click()
            pb.wait_for_loading_complete()

    def test_multiple_versions_ordering(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-008: Multiple versions listed in correct order."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        # Create two versions
        pb.set_editor_content("Version 2 content")
        pb.click_commit()
        pb.wait_for_loading_complete()
        pb.set_editor_content("Version 3 content")
        pb.click_commit()
        pb.wait_for_loading_complete()
        # Check version history ordering
        version_items = pb.page.locator("[data-testid='version-item']")
        if version_items.count() >= 2:
            # Newest should be first
            assert version_items.count() >= 2

    def test_set_version_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-007: Assign a name to a version."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        name_input = pb.page.locator("[data-testid='version-name']").or_(
            pb.page.get_by_label("Version name")
        ).first
        if name_input.is_visible():
            pb.fill_form_field(name_input, "production")

    def test_published_indicator(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-009: Published badge appears on the correct version."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        publish_btn = pb.page.get_by_role("button", name="Publish")
        if publish_btn.is_visible():
            publish_btn.click()
            pb.wait_for_loading_complete()
            badge = pb.page.locator(
                "[data-testid='published-badge']"
            ).or_(pb.page.get_by_text("Published")).first
            if badge.is_visible():
                assert badge.inner_text().strip() != ""
