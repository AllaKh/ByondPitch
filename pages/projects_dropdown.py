from playwright.sync_api import Page
from pages.base_page import BasePage


class ProjectsDropdown(BasePage):
    """
    Dropdown menu for selecting project.
    """

    QA_TEST_PROJECT = (
        "body > div.MuiPopover-root.MuiMenu-root.theme-scrollbar."
        "test--pageClients-blockProjectsPopup.MuiModal-root.rtl-6eo8t5 > "
        "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded."
        "MuiPaper-elevation8.MuiPopover-paper.MuiMenu-paper."
        "MuiMenu-paper.rtl-16911y2 > ul > div > "
        "li.MuiButtonBase-root.MuiMenuItem-root."
        "MuiMenuItem-gutters.test--buttonQA_Test_Project.rtl-aiuma > div"
    )

    def __init__(self, page: Page):
        super().__init__(page)

    def select_qa_test_project(self) -> None:
        """
        Select QA Test Project from dropdown.
        """
        self.click(self.QA_TEST_PROJECT)