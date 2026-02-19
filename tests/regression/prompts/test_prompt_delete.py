"""Regression tests for prompt deletion."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from utils.helpers import api_create_prompt, unique_name


@pytest.mark.regression
class TestPromptDelete:
    """Prompt deletion tests."""

    def test_delete_prompt_with_confirmation(
        self,
        authenticated_page: Page,
        base_url: str,
        api_url: str,
        guest_auth: dict,
        test_project: dict,
    ) -> None:
        """UI-PB-014: Delete prompt and confirm removal."""
        token = guest_auth["accessToken"]
        prompt_data = {
            "title": unique_name("del-prompt"),
            "content": "Content to delete",
            "description": "To be deleted",
        }
        prompt = api_create_prompt(api_url, token, test_project["id"], prompt_data)

        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        delete_btn = authenticated_page.get_by_role("button", name="Delete").first
        delete_btn.click()

        confirm_btn = authenticated_page.get_by_role("button", name="Confirm").or_(
            authenticated_page.get_by_role("button", name="Delete")
        ).first
        confirm_btn.click()

        authenticated_page.wait_for_load_state("networkidle")
        authenticated_page.wait_for_timeout(2000)
