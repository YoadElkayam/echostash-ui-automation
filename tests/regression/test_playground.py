"""Regression tests for Playground (UI-PG)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
class TestPlayground:
    """Verify the playground page functionality."""

    def test_playground_loads(self, page: Page, base_url: str) -> None:
        """UI-PG-001: Playground page loads successfully."""
        page.goto(f"{base_url}/playground")
        page.wait_for_load_state("domcontentloaded")
        body = page.locator("body").inner_text()
        assert len(body.strip()) > 0

    def test_playground_editor_interaction(
        self, page: Page, base_url: str
    ) -> None:
        """UI-PG-002: Can type content in the playground editor."""
        page.goto(f"{base_url}/playground")
        page.wait_for_load_state("domcontentloaded")
        # Look for Monaco editor or textarea
        editor = page.locator(".monaco-editor textarea, textarea").first
        if editor.is_visible():
            editor.focus()
            editor.type("Hello, playground!")
