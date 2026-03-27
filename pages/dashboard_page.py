from playwright.sync_api import Page
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """
    Page Object Model for Dashboard Manager page.
    Handles first visit fully, subsequent visits only verify URL.
    """

    SEARCH_INPUT = "#\\:ro\\:"
    TABLE_ROWS = "table tbody tr"
    ACTION_BUTTON_TEMPLATE = (
        "table tbody tr:has-text('{client}') td:nth-child(3) div button"
    )

    def __init__(self, page: Page):
        super().__init__(page)
        self._first_visit_done = False  # Flag for first visit

    def verify_loaded(self, expected_url: str) -> None:
        """
        Verify dashboard URL.
        On first visit, also wait for search input.
        """
        self.page.wait_for_url(expected_url)
        assert self.page.url == expected_url

        if not self._first_visit_done:
            self.wait_visible(self.SEARCH_INPUT)
            self._first_visit_done = True  # Mark first visit done

    def search_client(self, client_name: str) -> None:
        """
        Search client in the table.
        Only use on first visit when allowed.
        """
        if self._first_visit_done:
            # Skip searching on subsequent visits
            return

        self.fill(self.SEARCH_INPUT, client_name)
        result_selector = f"{self.TABLE_ROWS}:has-text('{client_name}')"
        self.wait_visible(result_selector)
        assert self.page.locator(result_selector).count() > 0

    def open_actions_menu(self, client_name: str) -> None:
        """
        Open the action button for a client.
        Only use on first visit when allowed.
        """
        if self._first_visit_done:
            # Skip opening actions on subsequent visits
            return

        selector = self.ACTION_BUTTON_TEMPLATE.format(client=client_name)
        self.wait_visible(selector)
        self.click(selector)