from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "/"):
        self.page.goto(path)

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")

    def screenshot(self, name: str):
        self.page.screenshot(path=f"test-results/{name}.png")
