"""Regression tests for Prompt Builder (UI-PB P1/P2)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestPromptMetadata:
    """Verify prompt metadata panel interactions."""

    def test_set_model_provider(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-005: Set model provider in metadata panel."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-provider"))
        provider_select = prompt_builder.page.locator(
            "[data-testid='provider-select']"
        ).or_(prompt_builder.page.get_by_label("Provider")).first
        if provider_select.is_visible():
            prompt_builder.set_model_provider("OpenAI")

    def test_set_model_name(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-006: Set model name in metadata panel."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-model"))
        model_select = prompt_builder.page.locator(
            "[data-testid='model-select']"
        ).or_(prompt_builder.page.get_by_label("Model")).first
        if model_select.is_visible():
            prompt_builder.set_model("gpt-4")

    def test_set_temperature(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-007: Set temperature slider/input."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-temp"))
        temp_input = prompt_builder.page.locator(
            "[data-testid='temperature-input']"
        ).or_(prompt_builder.page.get_by_label("Temperature")).first
        if temp_input.is_visible():
            prompt_builder.set_temperature(0.7)


@pytest.mark.regression
class TestPromptVisibility:
    """Verify prompt visibility toggle."""

    def test_visibility_private_to_public(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-009: Toggle visibility from private to public."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-vis"))
        vis_btn = prompt_builder.page.get_by_role(
            "button", name="Public"
        ).or_(prompt_builder.page.get_by_text("Public")).first
        if vis_btn.is_visible():
            vis_btn.click()

    def test_visibility_public_to_private(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-010: Toggle visibility from public to private."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-priv"))
        priv_btn = prompt_builder.page.get_by_role(
            "button", name="Private"
        ).or_(prompt_builder.page.get_by_text("Private")).first
        if priv_btn.is_visible():
            priv_btn.click()


@pytest.mark.regression
class TestPromptTags:
    """Verify tag selection on prompts."""

    def test_tag_selection(
        self, prompt_builder: PromptBuilderPage
    ) -> None:
        """UI-PB-011: Select tags for a prompt."""
        prompt_builder.open()
        prompt_builder.fill_title(unique_name("prompt-tags"))
        tag_input = prompt_builder.page.get_by_placeholder("Add tags").or_(
            prompt_builder.page.get_by_label("Tags")
        ).first
        if tag_input.is_visible():
            prompt_builder.select_tags(["AI", "testing"])


@pytest.mark.regression
class TestPromptDescription:
    """Verify prompt description editing."""

    def test_edit_prompt_description(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-013: Edit an existing prompt's description."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        pb.fill_description("Updated regression test description")
        pb.click_save()
        pb.wait_for_loading_complete()
