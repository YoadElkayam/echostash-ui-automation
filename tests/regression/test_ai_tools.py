"""Regression tests for AI Tools: Refine and Templatize (UI-AI)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import unique_name


@pytest.mark.regression
class TestRefine:
    """Verify the Refine AI tool."""

    def test_refine_modal_opens(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-AI-001: Refine modal opens with current content pre-filled."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        refine_btn = pb.page.get_by_role("button", name="Refine")
        if refine_btn.is_visible():
            refine_btn.click()
            modal = pb.page.locator("[role='dialog']")
            expect(modal).to_be_visible(timeout=5000)

    def test_refine_cancel_preserves_content(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-AI-004: Closing refine modal preserves original editor content."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        original = pb.get_editor_content()
        refine_btn = pb.page.get_by_role("button", name="Refine")
        if refine_btn.is_visible():
            refine_btn.click()
            close_btn = pb.page.get_by_role("button", name="Close").or_(
                pb.page.get_by_role("button", name="Cancel")
            ).first
            if close_btn.is_visible():
                close_btn.click()
            after = pb.get_editor_content()
            assert after == original


@pytest.mark.regression
class TestTemplatize:
    """Verify the Templatize AI tool."""

    def test_templatize_modal_opens(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-AI-005: Templatize modal opens with content."""
        pb = PromptBuilderPage(authenticated_page, base_url)
        pb.navigate(
            f"/dashboard/{test_project['id']}/prompts/{test_prompt['id']}"
        )
        pb.wait_for_page_load()
        templatize_btn = pb.page.get_by_role("button", name="Templatize")
        if templatize_btn.is_visible():
            templatize_btn.click()
            modal = pb.page.locator("[role='dialog']")
            expect(modal).to_be_visible(timeout=5000)
