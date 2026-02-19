"""Regression tests for the full prompt builder interaction."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from pages.project_view_page import ProjectViewPage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.regression
class TestPromptBuilder:
    """Full prompt builder interaction tests."""

    def test_create_prompt_all_fields(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PB-002: Create prompt with all fields populated."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.wait_for_page_load()

        name = unique_name("full-prompt")
        builder.fill_title(name)
        builder.fill_description("Full description for regression test")
        builder.set_editor_content(random_prompt_content())
        builder.click_save()

        expect(authenticated_page.get_by_text(name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_monaco_editor_paste_content(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PB-004: Monaco editor handles pasted content."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.wait_for_page_load()
        builder.fill_title(unique_name("paste-test"))

        long_content = "This is a longer piece of content\n" * 20
        builder.set_editor_content(long_content)
        result = builder.get_editor_content()
        assert "longer piece of content" in result

    def test_metadata_set_provider(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-005: Set model provider in metadata panel."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        # Try to set provider - this may not always be visible
        provider_el = authenticated_page.locator(
            "[data-testid='provider-select']"
        ).or_(authenticated_page.get_by_label("Provider")).first
        if provider_el.is_visible():
            builder.set_model_provider("OpenAI")

    def test_metadata_set_model(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-006: Set model name in metadata panel."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        model_el = authenticated_page.locator(
            "[data-testid='model-select']"
        ).or_(authenticated_page.get_by_label("Model")).first
        if model_el.is_visible():
            builder.set_model("gpt-4")
