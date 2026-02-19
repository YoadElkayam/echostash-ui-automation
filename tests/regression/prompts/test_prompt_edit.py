"""Regression tests for editing existing prompts."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestPromptEdit:
    """Prompt editing tests."""

    def test_edit_prompt_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-012: Edit existing prompt name."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        new_name = unique_name("edit-name")
        builder.fill_title(new_name)
        builder.click_save()

        expect(authenticated_page.get_by_text(new_name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_edit_prompt_description(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-013: Edit existing prompt description."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.fill_description("Updated description via automation")
        builder.click_save()
        authenticated_page.wait_for_timeout(2000)

    def test_edit_prompt_content(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """Edit prompt content in Monaco editor and save."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        new_content = "Updated prompt content: {{input}} with new instructions"
        builder.set_editor_content(new_content)
        builder.click_save()
        authenticated_page.wait_for_timeout(2000)

        result = builder.get_editor_content()
        assert "Updated prompt content" in result
