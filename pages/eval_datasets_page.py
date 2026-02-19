"""Page object for the Eval Datasets page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class EvalDatasetsPage(BasePage):
    """Manage evaluation datasets."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize EvalDatasetsPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Actions ──────────────────────────────────────────────────────────

    def create_dataset(self, name: str) -> None:
        """Create a new dataset.

        Args:
            name: Dataset name.
        """
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="New Dataset")
        ).first.click()
        name_input = self.page.get_by_label("Name").or_(
            self.page.get_by_placeholder("Dataset name")
        ).first
        self.fill_form_field(name_input, name)
        self.page.get_by_role("button", name="Create").or_(
            self.page.get_by_role("button", name="Save")
        ).first.click()
        self.wait_for_loading_complete()

    def import_csv(self, file_path: str) -> None:
        """Import a CSV file as dataset data.

        Args:
            file_path: Path to the CSV file to upload.
        """
        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(file_path)
        self.wait_for_loading_complete()

    def get_dataset_list(self) -> List[str]:
        """Return names of all datasets.

        Returns:
            List of dataset name strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='dataset-item']")
        return items.all_inner_texts()

    def click_dataset(self, name: str) -> None:
        """Click on a dataset by name.

        Args:
            name: Dataset name to click.
        """
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_for_loading_complete()

    def delete_dataset(self, name: str) -> None:
        """Delete a dataset by name.

        Args:
            name: Dataset name to delete.
        """
        row = self.page.get_by_text(name, exact=False).first
        row.hover()
        delete_btn = self.page.get_by_role("button", name="Delete").first
        delete_btn.click()
        # Confirm deletion
        self.page.get_by_role("button", name="Confirm").or_(
            self.page.get_by_role("button", name="Delete")
        ).first.click()
        self.wait_for_loading_complete()
