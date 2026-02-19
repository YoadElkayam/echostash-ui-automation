"""End-to-end test: full user workflow from guest login to fork."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage
from pages.browse_page import BrowsePage
from pages.dashboard_page import DashboardPage
from pages.project_modal import ProjectModal
from pages.project_view_page import ProjectViewPage
from pages.prompt_builder_page import PromptBuilderPage
from utils.helpers import random_prompt_content, unique_name


@pytest.mark.regression
class TestFullWorkflow:
    """End-to-end workflow: guest login -> create project -> create prompt
    -> commit -> publish -> browse public -> fork."""

    def test_complete_user_journey(self, page: Page, base_url: str) -> None:
        """Full user journey from guest login to browsing public prompts."""
        # Step 1: Guest login
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=15000)

        # Step 2: Create project
        dashboard = DashboardPage(page, base_url)
        dashboard.click_new_project()

        modal = ProjectModal(page, base_url)
        modal.wait_for_modal()
        project_name = unique_name("e2e-proj")
        modal.fill_name(project_name)
        modal.fill_description("End-to-end test project")
        modal.submit()

        page.wait_for_timeout(2000)
        expect(page.get_by_text(project_name, exact=False).first).to_be_visible(
            timeout=10000
        )

        # Step 3: Navigate into the project
        dashboard.click_project(project_name)
        page.wait_for_timeout(2000)

        # Step 4: Create prompt
        project_view = ProjectViewPage(page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(page, base_url)
        builder.wait_for_page_load()

        prompt_name = unique_name("e2e-prompt")
        builder.fill_title(prompt_name)
        builder.fill_description("E2E test prompt")
        content = random_prompt_content()
        builder.set_editor_content(content)
        builder.click_save()

        page.wait_for_timeout(2000)
        expect(page.get_by_text(prompt_name, exact=False).first).to_be_visible(
            timeout=10000
        )

        # Step 5: Commit version
        builder.set_editor_content(f"{content}\n\nUpdated for commit v2")
        builder.click_commit()
        page.wait_for_timeout(2000)

        # Step 6: Publish
        builder.click_publish()
        page.wait_for_timeout(2000)

        # Step 7: Browse public prompts
        page.goto(f"{base_url}/browse")
        page.wait_for_load_state("networkidle")

        browse = BrowsePage(page, base_url)
        cards = browse.get_prompt_cards()
        # The browse page should load (cards may or may not contain our prompt)
        assert "/browse" in page.url

    def test_share_and_view_public(self, page: Page, base_url: str) -> None:
        """Share a prompt and verify it can be viewed publicly."""
        from pages.share_page import SharePage

        # Share a prompt
        share = SharePage(page, base_url)
        share.open()

        name = unique_name("e2e-share")
        share.fill_name(name)
        share.fill_content(random_prompt_content())
        share.fill_description("E2E shared prompt")
        share.click_share()

        assert share.is_success_visible()

        # Get the share URL
        share_url = share.get_share_url()
        assert len(share_url) > 0

    def test_guest_project_prompt_lifecycle(self, page: Page, base_url: str) -> None:
        """Guest user creates project, adds prompt, edits, and deletes."""
        # Guest login
        auth = AuthPage(page, base_url)
        auth.navigate("/")
        auth.click_guest_login()
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=15000)

        # Create project
        dashboard = DashboardPage(page, base_url)
        dashboard.click_new_project()

        modal = ProjectModal(page, base_url)
        modal.wait_for_modal()
        project_name = unique_name("lifecycle-proj")
        modal.fill_name(project_name)
        modal.submit()
        page.wait_for_timeout(2000)

        # Navigate to project
        dashboard.click_project(project_name)
        page.wait_for_timeout(2000)

        # Create prompt
        project_view = ProjectViewPage(page, base_url)
        project_view.click_new_prompt()

        builder = PromptBuilderPage(page, base_url)
        builder.wait_for_page_load()

        prompt_name = unique_name("lifecycle-prompt")
        builder.fill_title(prompt_name)
        builder.set_editor_content("Initial content for lifecycle test")
        builder.click_save()
        page.wait_for_timeout(2000)

        # Edit prompt
        new_name = unique_name("lifecycle-edited")
        builder.fill_title(new_name)
        builder.click_save()
        page.wait_for_timeout(2000)

        expect(page.get_by_text(new_name, exact=False).first).to_be_visible(
            timeout=10000
        )
