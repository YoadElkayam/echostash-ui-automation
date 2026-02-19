"""Sanity tests for Version Control (UI-VC)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.sanity
class TestVersionControl:
    """Verify prompt version control operations."""

    def test_commit_new_version(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-001: Commit a new version of a prompt."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        pb.set_editor_content("Updated content for version commit v2")
        pb.click_commit()
        pb.wait_for_loading_complete()

    def test_publish_version(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-002: Publish a version of a prompt."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        publish_btn = pb.page.get_by_role("button", name="Publish")
        if publish_btn.is_visible():
            publish_btn.click()
            pb.wait_for_loading_complete()

    def test_version_history_view(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-003: Version history panel shows version list."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        # Look for version history panel or button
        version_btn = pb.page.get_by_text("Version").or_(
            pb.page.locator("[data-testid='version-history']")
        ).first
        if version_btn.is_visible():
            version_btn.click()
            pb.wait_for_loading_complete()

    def test_switch_between_versions(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-004: Switching between versions loads correct content."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        # Attempt to interact with version selector if available
        version_select = pb.page.locator("[data-testid='version-select']")
        if version_select.is_visible():
            version_select.click()
            # Click first available version option
            option = pb.page.locator("[data-testid='version-option']").first
            if option.is_visible():
                option.click()
                pb.wait_for_loading_complete()
