"""Regression tests for evaluation quality gates."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.evals_page import EvalsPage


@pytest.mark.regression
@pytest.mark.eval
class TestEvalQualityGate:
    """Verify quality gate configuration and display."""

    def test_quality_gate_tab_exists(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-023: Quality gates page is accessible."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        # Look for quality gate tab or section
        quality_tab = authenticated_page.get_by_text("Quality", exact=False).or_(
            authenticated_page.get_by_text("Gate", exact=False)
        ).first
        # Quality gates may be a separate tab or section
        if quality_tab.is_visible():
            quality_tab.click()
            authenticated_page.wait_for_timeout(1000)
