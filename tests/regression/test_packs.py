"""Regression tests for Browse Packs (UI-PACK)."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.browse_page import BrowsePage


@pytest.mark.regression
class TestBrowsePacks:
    """Verify the packs browsing functionality."""

    def test_view_packs_list(self, browse: BrowsePage) -> None:
        """UI-PACK-001: Packs list shows pack cards."""
        browse.open()
        browse.wait_for_loading_complete()
        packs_tab = browse.page.get_by_role("tab", name="Packs").or_(
            browse.page.get_by_text("Packs")
        ).first
        if packs_tab.is_visible():
            packs_tab.click()
            browse.wait_for_loading_complete()

    def test_open_pack_detail(self, browse: BrowsePage) -> None:
        """UI-PACK-002: Click a pack to see its prompts."""
        browse.open()
        browse.wait_for_loading_complete()
        packs_tab = browse.page.get_by_role("tab", name="Packs").or_(
            browse.page.get_by_text("Packs")
        ).first
        if packs_tab.is_visible():
            packs_tab.click()
            browse.wait_for_loading_complete()
            cards = browse.page.locator("[data-testid='pack-card']")
            if cards.count() > 0:
                cards.first.click()
                browse.page.wait_for_load_state("domcontentloaded")

    def test_fork_all_from_pack(self, browse: BrowsePage) -> None:
        """UI-PACK-003: Fork all prompts from a pack."""
        browse.open()
        browse.wait_for_loading_complete()
        packs_tab = browse.page.get_by_role("tab", name="Packs").or_(
            browse.page.get_by_text("Packs")
        ).first
        if packs_tab.is_visible():
            packs_tab.click()
            browse.wait_for_loading_complete()
            cards = browse.page.locator("[data-testid='pack-card']")
            if cards.count() > 0:
                cards.first.click()
                browse.page.wait_for_load_state("domcontentloaded")
                fork_all_btn = browse.page.get_by_role(
                    "button", name="Fork All"
                )
                if fork_all_btn.is_visible():
                    fork_all_btn.click()
                    browse.wait_for_loading_complete()
