from playwright.sync_api import Page


class BasePage:
    """
    Base page object providing common UI actions.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def wait_visible(self, selector: str) -> None:
        self.page.wait_for_selector(selector, state="visible")

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()