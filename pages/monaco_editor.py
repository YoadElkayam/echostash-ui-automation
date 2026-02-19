"""Helper for interacting with Monaco Editor instances."""

from __future__ import annotations

from playwright.sync_api import Page


class MonacoEditor:
    """Provides methods to interact with a Monaco Editor embedded in the page."""

    EDITOR_SELECTOR = ".monaco-editor"

    def __init__(self, page: Page) -> None:
        """Initialize MonacoEditor helper.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    def wait_for_ready(self, timeout: int = 15000) -> None:
        """Wait for the Monaco editor to be loaded and visible.

        Args:
            timeout: Maximum wait time in milliseconds.
        """
        self.page.locator(self.EDITOR_SELECTOR).first.wait_for(
            state="visible", timeout=timeout
        )

    def set_value(self, text: str) -> None:
        """Set the editor value programmatically via the Monaco API.

        Args:
            text: Content to set in the editor.
        """
        self.wait_for_ready()
        self.page.evaluate(
            """(val) => {
                const editor = window.monaco?.editor?.getEditors()?.[0];
                if (editor) {
                    editor.setValue(val);
                }
            }""",
            text,
        )

    def get_value(self) -> str:
        """Get the current editor value via the Monaco API.

        Returns:
            Editor content as a string.
        """
        self.wait_for_ready()
        return self.page.evaluate(
            """() => {
                const editor = window.monaco?.editor?.getEditors()?.[0];
                return editor ? editor.getValue() : '';
            }"""
        )

    def type_text(self, text: str) -> None:
        """Simulate typing text into the editor.

        Args:
            text: Text to type character by character.
        """
        self.wait_for_ready()
        editor_el = self.page.locator(f"{self.EDITOR_SELECTOR} textarea").first
        editor_el.focus()
        editor_el.type(text)

    def clear(self) -> None:
        """Clear all editor content."""
        self.set_value("")

    def get_line_count(self) -> int:
        """Get the number of lines in the editor.

        Returns:
            Number of lines.
        """
        self.wait_for_ready()
        return self.page.evaluate(
            """() => {
                const editor = window.monaco?.editor?.getEditors()?.[0];
                return editor ? editor.getModel().getLineCount() : 0;
            }"""
        )
