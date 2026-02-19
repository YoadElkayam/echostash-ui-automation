"""Page object for the Prompt Builder page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.monaco_editor import MonacoEditor


class PromptBuilderPage(BasePage):
    """Prompt Builder page for creating and editing prompts."""

    PATH = "/prompt-builder"

    def __init__(self, page: Page, base_url: str = "") -> None:
        """Initialize PromptBuilderPage.

        Args:
            page: Playwright page instance.
            base_url: Application base URL.
        """
        super().__init__(page, base_url)
        self.editor = MonacoEditor(page)

    def open(self) -> None:
        """Navigate to the prompt builder."""
        self.navigate(self.PATH)
        self.wait_for_page_load()

    # ── Locators ─────────────────────────────────────────────────────────

    @property
    def _title_input(self):
        """Prompt title input."""
        return self.page.get_by_label("Title").or_(
            self.page.get_by_placeholder("Prompt title")
        ).first

    @property
    def _description_input(self):
        """Prompt description input."""
        return self.page.get_by_label("Description").or_(
            self.page.get_by_placeholder("Description")
        ).first

    @property
    def _save_btn(self):
        """Save button."""
        return self.page.get_by_role("button", name="Save")

    @property
    def _publish_btn(self):
        """Publish button."""
        return self.page.get_by_role("button", name="Publish")

    @property
    def _commit_btn(self):
        """Commit button."""
        return self.page.get_by_role("button", name="Commit")

    @property
    def _refine_btn(self):
        """Refine button."""
        return self.page.get_by_role("button", name="Refine")

    @property
    def _templatize_btn(self):
        """Templatize button."""
        return self.page.get_by_role("button", name="Templatize")

    # ── Actions ──────────────────────────────────────────────────────────

    def fill_title(self, title: str) -> None:
        """Fill the prompt title field.

        Args:
            title: Prompt title text.
        """
        self.fill_form_field(self._title_input, title)

    def fill_description(self, description: str) -> None:
        """Fill the prompt description field.

        Args:
            description: Prompt description text.
        """
        self.fill_form_field(self._description_input, description)

    def set_visibility(self, visibility: str) -> None:
        """Set prompt visibility (private or public).

        Args:
            visibility: Either 'private' or 'public'.
        """
        vis_btn = self.page.get_by_role("button", name=visibility.capitalize()).or_(
            self.page.get_by_text(visibility, exact=False)
        ).first
        vis_btn.click()

    def select_tags(self, tags: List[str]) -> None:
        """Select tags for the prompt.

        Args:
            tags: List of tag names to select.
        """
        tag_input = self.page.get_by_placeholder("Add tags").or_(
            self.page.get_by_label("Tags")
        ).first
        for tag in tags:
            tag_input.fill(tag)
            self.page.keyboard.press("Enter")

    def set_model_provider(self, provider: str) -> None:
        """Select the model provider.

        Args:
            provider: Provider name (e.g. 'OpenAI', 'Anthropic').
        """
        provider_select = self.page.locator("[data-testid='provider-select']").or_(
            self.page.get_by_label("Provider")
        ).first
        provider_select.click()
        self.page.get_by_text(provider, exact=False).first.click()

    def set_model(self, model: str) -> None:
        """Select the model.

        Args:
            model: Model name (e.g. 'gpt-4', 'claude-3').
        """
        model_select = self.page.locator("[data-testid='model-select']").or_(
            self.page.get_by_label("Model")
        ).first
        model_select.click()
        self.page.get_by_text(model, exact=False).first.click()

    def set_temperature(self, temp: float) -> None:
        """Set the temperature slider/input value.

        Args:
            temp: Temperature value (0.0 - 2.0).
        """
        temp_input = self.page.locator("[data-testid='temperature-input']").or_(
            self.page.get_by_label("Temperature")
        ).first
        temp_input.fill(str(temp))

    def get_editor_content(self) -> str:
        """Get the current content from the Monaco editor.

        Returns:
            Editor content as string.
        """
        return self.editor.get_value()

    def set_editor_content(self, content: str) -> None:
        """Set content in the Monaco editor.

        Args:
            content: Content to set in the editor.
        """
        self.editor.set_value(content)

    def click_save(self) -> None:
        """Click the Save button."""
        self._save_btn.click()
        self.wait_for_loading_complete()

    def click_publish(self) -> None:
        """Click the Publish button."""
        self._publish_btn.click()
        self.wait_for_loading_complete()

    def click_commit(self) -> None:
        """Click the Commit button."""
        self._commit_btn.click()
        self.wait_for_loading_complete()

    def toggle_editor_mode(self) -> None:
        """Toggle between editor modes (e.g. raw / visual)."""
        toggle = self.page.locator("[data-testid='editor-mode-toggle']").or_(
            self.page.get_by_role("switch")
        ).first
        toggle.click()

    def click_refine(self) -> None:
        """Click the Refine button."""
        self._refine_btn.click()
        self.wait_for_loading_complete()

    def click_templatize(self) -> None:
        """Click the Templatize button."""
        self._templatize_btn.click()
        self.wait_for_loading_complete()

    def get_version_number(self) -> str:
        """Get the current version number displayed.

        Returns:
            Version number string.
        """
        version_el = self.page.locator("[data-testid='version-number']").or_(
            self.page.get_by_text("Version")
        ).first
        return self.get_text(version_el)

    def select_version(self, version: str) -> None:
        """Select a specific version from the version selector.

        Args:
            version: Version identifier to select.
        """
        version_select = self.page.locator("[data-testid='version-select']")
        version_select.click()
        self.page.get_by_text(version, exact=False).first.click()

    def open_in_playground(self) -> None:
        """Open the current prompt in the playground."""
        playground_btn = self.page.get_by_role("button", name="Playground").or_(
            self.page.get_by_text("Open in Playground")
        ).first
        playground_btn.click()
        self.wait_for_page_load()
