"""Regression tests for evaluation runs."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.eval_runs_page import EvalRunsPage
from pages.evals_page import EvalsPage


@pytest.mark.regression
@pytest.mark.eval
class TestEvalRuns:
    """Verify eval run execution and results."""

    def test_view_runs_list(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-018: View runs list."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate_tab("Runs")

        runs = EvalRunsPage(authenticated_page, base_url)
        run_list = runs.get_run_list()
        assert isinstance(run_list, list)

    def test_navigate_eval_tabs(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """Navigate between eval tabs."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        evals = EvalsPage(authenticated_page, base_url)

        for tab in ["Datasets", "Suites", "Runs"]:
            evals.navigate_tab(tab)
            authenticated_page.wait_for_timeout(500)
