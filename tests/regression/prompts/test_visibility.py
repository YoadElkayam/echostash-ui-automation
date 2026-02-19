"""Regression tests for prompt visibility toggle."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage


@pytest.mark.regression
class TestPromptVisibility:
    """Verify prompt visibility toggle (private/public)."""

    def test_toggle_private_to_public(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-009: Toggle visibility from private to public."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.set_visibility("public")
        builder.click_save()
        authenticated_page.wait_for_timeout(2000)

    def test_toggle_public_to_private(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-010: Toggle visibility from public to private."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.set_visibility("private")
        builder.click_save()
        authenticated_page.wait_for_timeout(2000)
