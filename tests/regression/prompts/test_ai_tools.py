"""Regression tests for AI tools (Refine and Templatize)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import random_prompt_content


@pytest.mark.regression
class TestRefine:
    """Verify Refine modal functionality."""

    def test_refine_modal_open(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-AI-001: Refine modal opens with content."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.set_editor_content(random_prompt_content())

        refine_btn = authenticated_page.get_by_role("button", name="Refine")
        if refine_btn.is_visible():
            refine_btn.click()
            authenticated_page.wait_for_timeout(1000)
            # Modal should be visible
            modal = authenticated_page.locator("[role='dialog']")
            expect(modal).to_be_visible(timeout=5000)

    def test_refine_cancel(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-AI-004: Closing refine modal keeps content unchanged."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        original_content = random_prompt_content()
        builder.set_editor_content(original_content)

        refine_btn = authenticated_page.get_by_role("button", name="Refine")
        if refine_btn.is_visible():
            refine_btn.click()
            authenticated_page.wait_for_timeout(500)

            close_btn = authenticated_page.locator(
                "[role='dialog'] button[aria-label='Close']"
            ).or_(
                authenticated_page.locator("[role='dialog'] button:has-text('Close')")
            ).or_(
                authenticated_page.locator("[role='dialog'] button:has-text('Cancel')")
            ).first
            if close_btn.is_visible():
                close_btn.click()

            result = builder.get_editor_content()
            assert original_content in result


@pytest.mark.regression
class TestTemplatize:
    """Verify Templatize modal functionality."""

    def test_templatize_modal_open(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-AI-005: Templatize modal opens."""
        authenticated_page.goto(
            f"{base_url}/dashboard/{test_project['id']}/{test_prompt['id']}"
        )
        authenticated_page.wait_for_load_state("networkidle")

        builder = PromptBuilderPage(authenticated_page, base_url)
        builder.set_editor_content(random_prompt_content())

        templatize_btn = authenticated_page.get_by_role("button", name="Templatize")
        if templatize_btn.is_visible():
            templatize_btn.click()
            authenticated_page.wait_for_timeout(1000)
            modal = authenticated_page.locator("[role='dialog']")
            expect(modal).to_be_visible(timeout=5000)
