"""Regression tests for evaluation suites."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.eval_suites_page import EvalSuitesPage
from pages.evals_page import EvalsPage
from utils.helpers import unique_name


@pytest.mark.regression
@pytest.mark.eval
class TestEvalSuites:
    """Verify eval suite CRUD operations."""

    def test_create_suite(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-009: Create a new evaluation suite."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate_tab("Suites")

        suites = EvalSuitesPage(authenticated_page, base_url)
        name = unique_name("suite")
        suites.create_suite(name)
        authenticated_page.wait_for_timeout(2000)

    def test_view_suite_list(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-010: View suite list."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate_tab("Suites")

        suites = EvalSuitesPage(authenticated_page, base_url)
        suite_list = suites.get_suite_list()
        assert isinstance(suite_list, list)
