"""Page object for the Eval Runs page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage


class EvalRunsPage(BasePage):
    """Manage and monitor evaluation runs."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize EvalRunsPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Actions ──────────────────────────────────────────────────────────

    def run_suite(self, suite_name: str) -> None:
        """Start a run for a given suite.

        Args:
            suite_name: Name of the suite to run.
        """
        self.page.get_by_role("button", name="Run").or_(
            self.page.get_by_role("button", name="Start Run")
        ).first.click()
        self.page.get_by_text(suite_name, exact=False).first.click()
        self.page.get_by_role("button", name="Start").or_(
            self.page.get_by_role("button", name="Run")
        ).first.click()
        self.wait_for_loading_complete()

    def get_run_list(self) -> List[str]:
        """Return identifiers/labels of all runs.

        Returns:
            List of run label strings.
        """
        self.wait_for_loading_complete()
        items = self.page.locator("[data-testid='run-item']")
        return items.all_inner_texts()

    def click_run(self, index: int) -> None:
        """Click on a run by index.

        Args:
            index: Zero-based index of the run to click.
        """
        items = self.page.locator("[data-testid='run-item']")
        items.nth(index).click()
        self.wait_for_loading_complete()

    def get_run_status(self, run_id: str) -> str:
        """Get the status of a specific run.

        Args:
            run_id: Run identifier.

        Returns:
            Status string (e.g. 'running', 'completed', 'failed').
        """
        status_el = self.page.locator(f"[data-testid='run-status-{run_id}']")
        if status_el.is_visible():
            return status_el.inner_text().lower()
        return ""

    def wait_for_run_complete(self, run_id: str, timeout: int = 120000) -> None:
        """Wait for a run to reach completed status.

        Args:
            run_id: Run identifier.
            timeout: Maximum wait time in milliseconds.
        """
        status_el = self.page.locator(f"[data-testid='run-status-{run_id}']")
        status_el.filter(has_text="completed").wait_for(
            state="visible", timeout=timeout
        )
