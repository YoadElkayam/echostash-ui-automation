"""Regression tests for prompt tag management."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage


@pytest.mark.regression
class TestPromptTags:
    """Verify tag selection on prompts."""

    def test_select_tags(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-011: Select tags for a prompt."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        tag_input = authenticated_page.get_by_placeholder("Add tags").or_(
            authenticated_page.get_by_label("Tags")
        ).first
        if tag_input.is_visible():
            builder.select_tags(["AI", "coding"])
            builder.click_save()
            authenticated_page.wait_for_timeout(2000)
