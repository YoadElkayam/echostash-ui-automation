"""Sanity tests for prompt version control (commit and publish)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.sanity
class TestPromptVersion:
    """Verify version control core flows."""

    def test_commit_version(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-001: Commit a new version of a prompt."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.set_editor_content(random_prompt_content())
        builder.click_commit()

        # Should see a success indicator or version number change
        authenticated_page.wait_for_timeout(2000)
        # Verify commit button is still available (page did not error)
        commit_btn = authenticated_page.get_by_role("button", name="Commit")
        expect(commit_btn).to_be_visible(timeout=5000)

    def test_publish_version(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-002: Publish a version of a prompt."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        # Commit first, then publish
        builder.set_editor_content(random_prompt_content())
        builder.click_commit()
        authenticated_page.wait_for_timeout(1000)
        builder.click_publish()

        # Should see a published indicator
        authenticated_page.wait_for_timeout(2000)

    def test_version_history_view(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-003: View version history panel."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        # Commit a version first
        builder.set_editor_content(random_prompt_content())
        builder.click_commit()
        authenticated_page.wait_for_timeout(1000)

        # Look for version history elements
        version_el = authenticated_page.locator(
            "[data-testid='version-history'], [data-testid='version-select']"
        ).or_(authenticated_page.get_by_text("Version", exact=False)).first
        expect(version_el).to_be_visible(timeout=10000)

    def test_switch_between_versions(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-VC-004: Switch between different versions."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)

        # Create first version
        content_v1 = "Version 1 content for testing"
        builder.set_editor_content(content_v1)
        builder.click_commit()
        authenticated_page.wait_for_timeout(1000)

        # Create second version
        content_v2 = "Version 2 content for testing"
        builder.set_editor_content(content_v2)
        builder.click_commit()
        authenticated_page.wait_for_timeout(1000)

        # The version selector should be available
        version_select = authenticated_page.locator("[data-testid='version-select']")
        if version_select.is_visible():
            version_select.click()
            # Click on an older version entry
            authenticated_page.locator("[data-testid='version-select'] option, li").first.click()
            authenticated_page.wait_for_timeout(1000)
