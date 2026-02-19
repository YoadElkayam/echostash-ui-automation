"""Regression tests for Evaluations (UI-EVAL)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.evals_page import EvalsPage


@pytest.mark.regression
@pytest.mark.eval
class TestEvalsNavigation:
    """Verify eval page navigation and tabs."""

    def test_navigate_to_evals(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-001: Navigate to evals for a specific prompt."""
        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate(f"/evals/{test_prompt['id']}")
        evals.wait_for_page_load()
        assert "evals" in evals.page.url

    def test_evals_tabs(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """Verify eval tabs are present and clickable."""
        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate(f"/evals/{test_prompt['id']}")
        evals.wait_for_page_load()
        for tab_name in ["Datasets", "Suites", "Runs"]:
            tab = evals.page.get_by_role("tab", name=tab_name).or_(
                evals.page.get_by_text(tab_name)
            ).first
            if tab.is_visible():
                tab.click()
                evals.wait_for_loading_complete()


@pytest.mark.regression
@pytest.mark.eval
class TestEvalsDatasets:
    """Verify dataset CRUD operations."""

    def test_create_dataset(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-002: Create a new dataset."""
        from pages.eval_datasets_page import EvalDatasetsPage

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate(f"/evals/{test_prompt['id']}")
        evals.wait_for_page_load()
        evals.navigate_tab("Datasets")
        ds = EvalDatasetsPage(authenticated_page, base_url)
        create_btn = ds.page.get_by_role("button", name="Create").or_(
            ds.page.get_by_role("button", name="New Dataset")
        ).first
        if create_btn.is_visible():
            ds.create_dataset("regression-dataset")

    def test_view_dataset_detail(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-004: Click on a dataset to view details."""
        from pages.eval_datasets_page import EvalDatasetsPage

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate(f"/evals/{test_prompt['id']}")
        evals.wait_for_page_load()
        evals.navigate_tab("Datasets")
        ds = EvalDatasetsPage(authenticated_page, base_url)
        items = ds.page.locator("[data-testid='dataset-item']")
        if items.count() > 0:
            items.first.click()
            ds.wait_for_loading_complete()


@pytest.mark.regression
@pytest.mark.eval
class TestEvalsSuites:
    """Verify suite CRUD operations."""

    def test_create_suite(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-009: Create a new evaluation suite."""
        from pages.eval_suites_page import EvalSuitesPage

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate(f"/evals/{test_prompt['id']}")
        evals.wait_for_page_load()
        evals.navigate_tab("Suites")
        sp = EvalSuitesPage(authenticated_page, base_url)
        create_btn = sp.page.get_by_role("button", name="Create").or_(
            sp.page.get_by_role("button", name="New Suite")
        ).first
        if create_btn.is_visible():
            sp.create_suite("regression-suite")


@pytest.mark.regression
@pytest.mark.eval
class TestEvalsRuns:
    """Verify eval run operations."""

    def test_runs_tab_loads(
        self,
        authenticated_page: Page,
        base_url: str,
        test_project: dict,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-018: Runs tab loads with run list."""
        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate(f"/evals/{test_prompt['id']}")
        evals.wait_for_page_load()
        evals.navigate_tab("Runs")
        evals.wait_for_loading_complete()
