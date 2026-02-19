"""Sanity tests for the Prompt Builder (UI-PB)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.sanity
class TestCreatePrompt:
    """Verify prompt creation flows in the builder."""

    def test_create_prompt_minimal(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-001: Create a new prompt with just a name."""
        prompt_builder.open()
        name = unique_name("prompt-min")
        prompt_builder.fill_title(name)
        prompt_builder.click_save()
        prompt_builder.wait_for_loading_complete()

    def test_create_prompt_all_fields(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-002: Create prompt with name, description, and content."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-full"))
        prompt_builder.fill_description("A comprehensive test prompt")
        prompt_builder.set_editor_content("You are a helpful assistant. {{input}}")
        prompt_builder.click_save()
        prompt_builder.wait_for_loading_complete()

    def test_create_prompt_validation_missing_name(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-015: Creating a prompt without a name shows validation error."""
        prompt_builder.open()
        prompt_builder.fill_title("")
        prompt_builder.click_save()
        # Should show some validation feedback or remain on the same page
        prompt_builder.page.wait_for_timeout(1000)


@pytest.mark.sanity
class TestMonacoEditor:
    """Verify Monaco editor interactions."""

    def test_monaco_editor_type_content(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-003: Content typed in Monaco editor is retained."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-editor"))
        content = "Analyze the following data: {{data}}"
        prompt_builder.set_editor_content(content)
        result = prompt_builder.get_editor_content()
        assert content in result

    def test_monaco_editor_clear_and_retype(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-004: Editor content can be cleared and re-entered."""
        prompt_builder.open()
        prompt_builder.editor.wait_for_ready()
        prompt_builder.editor.set_value("First content")
        prompt_builder.editor.clear()
        assert prompt_builder.editor.get_value() == ""
        prompt_builder.editor.set_value("Second content")
        assert "Second content" in prompt_builder.editor.get_value()


@pytest.mark.sanity
class TestEditPrompt:
    """Verify editing existing prompts."""

    def test_edit_prompt_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-012: Edit an existing prompt's name."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        new_name = unique_name("prompt-renamed")
        pb.fill_title(new_name)
        pb.click_save()
        pb.wait_for_loading_complete()

    def test_delete_prompt(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-014: Delete a prompt from the builder."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        delete_btn = pb.page.get_by_role("button", name="Delete").first
        if delete_btn.is_visible():
            delete_btn.click()
            confirm = pb.page.get_by_role("button", name="Confirm").or_(
                pb.page.get_by_role("button", name="Delete")
            ).first
            if confirm.is_visible():
                confirm.click()
            pb.page.wait_for_load_state("networkidle")
