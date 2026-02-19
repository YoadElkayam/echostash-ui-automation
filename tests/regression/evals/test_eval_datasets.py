"""Regression tests for evaluation datasets."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.eval_datasets_page import EvalDatasetsPage
from pages.evals_page import EvalsPage
from utils.helpers import unique_name


@pytest.mark.regression
@pytest.mark.eval
class TestEvalDatasets:
    """Verify eval dataset CRUD operations."""

    def test_navigate_to_evals(
        self,
        authenticated_page: Page,
        base_url: str,
    ) -> None:
        """UI-EVAL-001: Navigate to evals page."""
        evals = EvalsPage(authenticated_page, base_url)
        evals.open()
        expect(authenticated_page).to_have_url(f"{base_url}/evals", timeout=10000)

    def test_create_dataset(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-002: Create a new dataset."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate_tab("Datasets")

        datasets = EvalDatasetsPage(authenticated_page, base_url)
        name = unique_name("dataset")
        datasets.create_dataset(name)
        authenticated_page.wait_for_timeout(2000)

    def test_view_dataset_list(
        self,
        authenticated_page: Page,
        base_url: str,
        test_prompt: dict,
    ) -> None:
        """UI-EVAL-004: View dataset list."""
        authenticated_page.goto(f"{base_url}/evals/{test_prompt['id']}")
        authenticated_page.wait_for_load_state("networkidle")

        evals = EvalsPage(authenticated_page, base_url)
        evals.navigate_tab("Datasets")

        datasets = EvalDatasetsPage(authenticated_page, base_url)
        dataset_list = datasets.get_dataset_list()
        assert isinstance(dataset_list, list)
