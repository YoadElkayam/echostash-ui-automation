"""Page object for the create/edit project modal dialog."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class ProjectModal(BasePage):
    """Modal dialog for creating or editing a project."""

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize ProjectModal.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _modal(self):
        """The modal dialog element."""
        return self.page.locator("[role='dialog']")

    @property
    def _name_input(self):
        """Project name input field."""
        return self._modal.get_by_label("Name").or_(
            self._modal.get_by_placeholder("Project name")
        ).first

    @property
    def _description_input(self):
        """Project description input field."""
        return self._modal.get_by_label("Description").or_(
            self._modal.get_by_placeholder("Description")
        ).first

    @property
    def _submit_btn(self):
        """Submit / Create button."""
        return self._modal.get_by_role("button", name="Create").or_(
            self._modal.get_by_role("button", name="Save")
        ).first

    @property
    def _cancel_btn(self):
        """Cancel button."""
        return self._modal.get_by_role("button", name="Cancel")

    # ── Actions ──────────────────────────────────────────────────────────

    def wait_for_modal(self, timeout: int = 5000) -> None:
        """Wait for the project modal to appear.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        self._modal.wait_for(state="visible", timeout=timeout)

    def fill_name(self, name: str) -> None:
        """Fill the project name field.

        Args:
            name: Project name.
        """
        self.fill_form_field(self._name_input, name)

    def fill_description(self, description: str) -> None:
        """Fill the project description field.

        Args:
            description: Project description.
        """
        self.fill_form_field(self._description_input, description)

    def submit(self) -> None:
        """Click the submit button and wait for the modal to close."""
        self._submit_btn.click()
        self._modal.wait_for(state="hidden", timeout=10000)

    def cancel(self) -> None:
        """Click the cancel button."""
        self._cancel_btn.click()
        self._modal.wait_for(state="hidden")
