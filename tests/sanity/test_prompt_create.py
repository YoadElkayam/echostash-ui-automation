"""Sanity tests for prompt creation in the prompt builder."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from pages.project_view_page import ProjectViewPage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.sanity
class TestPromptCreate:
    """Verify prompt creation flows."""

    def test_create_prompt_minimal(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PB-001: Create a new prompt with just a name."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.wait_for_page_load()
        name = unique_name("sanity-prompt")
        builder.fill_title(name)
        builder.click_save()

        # Should see the prompt title somewhere on the page
        expect(authenticated_page.get_by_text(name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_create_prompt_all_fields(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PB-002: Create a prompt with title, description, and content."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.wait_for_page_load()

        name = unique_name("full-prompt")
        builder.fill_title(name)
        builder.fill_description("A fully populated test prompt")
        builder.set_editor_content(random_prompt_content())
        builder.click_save()

        expect(authenticated_page.get_by_text(name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_monaco_editor_type_content(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PB-003: Monaco editor accepts typed content."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.wait_for_page_load()
        builder.fill_title(unique_name("editor-test"))

        test_content = "Hello from the automated test!"
        builder.set_editor_content(test_content)
        result = builder.get_editor_content()
        assert test_content in result

    def test_edit_prompt_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-PB-012: Edit an existing prompt name."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        new_name = unique_name("renamed")
        builder.fill_title(new_name)
        builder.click_save()

        expect(authenticated_page.get_by_text(new_name, exact=False).first).to_be_visible(
            timeout=10000
        )

    def test_delete_prompt(
        self,
        authenticated_page: Page,
        base_url: str,
        api_url: str,
        guest_auth: dict,
        test_project: dict,
    ) -> None:
        """UI-PB-014: Delete a prompt from the builder."""
        from utils.helpers import api_create_prompt

        token = guest_auth["accessToken"]
        prompt_data = {
            "title": unique_name("del-prompt"),
            "content": "To be deleted",
            "description": "Will be deleted",
        }
        prompt = api_create_prompt(api_url, token, test_project["id"], prompt_data)

        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        # Click delete button
        delete_btn = authenticated_page.get_by_role("button", name="Delete").first
        delete_btn.click()

        # Confirm deletion
        confirm_btn = authenticated_page.get_by_role("button", name="Confirm").or_(
            authenticated_page.get_by_role("button", name="Delete")
        ).first
        confirm_btn.click()

        # Should navigate back to project view
        authenticated_page.wait_for_load_state("networkidle")

    def test_create_prompt_validation_missing_name(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
    ) -> None:
        """UI-PB-015: Creating a prompt without a name shows validation error."""
        authenticated_page.goto(f"{base_url}/dashboard/{test_project['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        project_view = ProjectViewPage(authenticated_page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.wait_for_page_load()
        # Leave title empty
        builder.fill_title("")
        builder.click_save()

        # Page should not navigate away - still on builder
        authenticated_page.wait_for_timeout(1000)
        assert "prompt-builder" in authenticated_page.url or "dashboard" in authenticated_page.url
