from playwright.sync_api import Page
from pages.base_page import BasePage


class StartMeetingDialog(BasePage):
    """
    Modal dialog for starting meeting.
    """

    OK_BUTTON = (
        "body > div.MuiDialog-root.test--pageClients-blockStartMeetingDialog."
        "MuiModal-root.rtl-nzmaea > div.MuiDialog-container."
        "MuiDialog-scrollBody.rtl-ruoso9 > div > "
        "div.MuiDialogActions-root.MuiDialogActions-spacing."
        "rtl-1v4kc3k > "
        "button.MuiButtonBase-root.MuiButton-root."
        "MuiButton-contained.MuiButton-containedPrimary."
        "MuiButton-sizeMedium.MuiButton-containedSizeMedium."
        "MuiButton-colorPrimary.test--buttonOk.rtl-fydyy0"
    )

    START_MEETING_TEXT = "text=התחל פגישה"

    def __init__(self, page: Page):
        super().__init__(page)

    def confirm_start_meeting(self) -> None:
        """
        Click OK button in start meeting dialog.
        """
        self.click(self.OK_BUTTON)

    def wait_for_start_meeting_text(self) -> None:
        """
        Wait until 'Start Meeting' text appears.
        """
        self.page.wait_for_selector(self.START_MEETING_TEXT)