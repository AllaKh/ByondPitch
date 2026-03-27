from playwright.sync_api import Page
from pages.base_page import BasePage
from datetime import datetime
from config import DASHBOARD_URL

class MeetingRoomPage(BasePage):
    """
    Page Object Model for active meeting room.
    """

    WAITING_PARTICIPANT_TITLE = "#__next h5"
    ACCEPT_PARTICIPANT_BUTTON = "div.waiting-participant button"
    CONFIRM_ACCEPT_BUTTON = "div.MuiDialog-root button.test--buttonOk"
    END_CALL_BUTTON = "div.call-control-bar button"

    WARNING_DIALOG = "div.MuiDialog-root.MuiModal-root.rtl-nzmaea"
    WARNING_CONFIRM_BUTTON = (
        "div.MuiDialog-root.MuiModal-root.rtl-nzmaea button.test--buttonOk"
    )

    POST_CALL_DIALOG = "div.MuiDialog-root.MuiModal-root.rtl-1z0ys3a"

    def __init__(self, page: Page):
        super().__init__(page)

    def wait_for_waiting_participant(self) -> None:
        self.wait_visible(self.WAITING_PARTICIPANT_TITLE)

    def accept_participant(self) -> None:
        self.page.locator(self.ACCEPT_PARTICIPANT_BUTTON).first.click(force=True)
        self.page.wait_for_selector(self.CONFIRM_ACCEPT_BUTTON, state="visible")
        self.page.locator(self.CONFIRM_ACCEPT_BUTTON).click(force=True)
        self.page.wait_for_selector("div.MuiDialog-root", state="hidden")

    def end_call(self) -> None:
        """
        Complete end call flow including task creation.
        """

        # Wait for End Call button
        self.page.wait_for_selector(self.END_CALL_BUTTON, state="visible")
        self.page.wait_for_timeout(1500)

        # Click End Call
        self.page.locator(self.END_CALL_BUTTON).last.click(force=True)
        self.page.wait_for_timeout(2000)

        # Wait for Warning dialog
        self.page.wait_for_selector(self.WARNING_DIALOG, state="visible")

        # Verify warning text
        warning_text = self.page.inner_text(self.WARNING_DIALOG)
        assert "אזהרה" in warning_text
        assert "האם אתה בטוח שברצונך לצאת מהשיחה?" in warning_text

        # Click אישור
        self.page.locator(self.WARNING_CONFIRM_BUTTON).click(force=True)
        self.page.wait_for_selector(self.WARNING_DIALOG, state="hidden")

        # Wait for Post Call dialog
        self.page.wait_for_selector(self.POST_CALL_DIALOG, state="visible")

        post_text = self.page.inner_text(self.POST_CALL_DIALOG)
        assert "סיום פגישה" in post_text
        assert "השיחה לא התקיימה" in post_text

        # Click משימה ותזכורת
        self.page.locator("div.MuiBox-root.rtl-1o9nvex button").click(force=True)
        self.page.wait_for_timeout(1500)

        # ---- Fill Subject (נושא) ----
        subject_input = self.page.get_by_placeholder("נושא")
        subject_input.wait_for(state="visible")
        subject_input.fill("שיחה עם אלה חננשווילי")

        # ---- Fill Description (תיאור) ----
        dialog = self.page.locator("div.MuiDialog-root")
        description_input = dialog.get_by_label("תיאור")
        description_input.wait_for(state="visible")
        description_input.fill("הצעה מסחרית להחלפת ספק")

        # ---- Fill DateTime directly ----
        now = datetime.now()
        formatted_now = now.strftime("%m/%d/%Y %H:%M")
        date_input = dialog.get_by_placeholder("MM/DD/YYYY hh:mm")
        date_input.wait_for(state="visible")
        date_input.fill(formatted_now)
        date_input.press("Enter")

        self.page.wait_for_timeout(1000)

        # ---- Fill Description (תיאור) second input ----
        description_input_2 = dialog.locator("div.MuiFormControl-fullWidth input").nth(1)
        description_input_2.wait_for(state="visible")
        description_input_2.fill("הצעה מסחרית להחלפת ספק")

        # ---- Click סיום פגישה ----
        self.page.locator("div.MuiDialogActions-root.rtl-10sjoy4 > button").click(force=True)

        # ---- Wait until all dialogs close ----
        dialog.wait_for(state="hidden")

        # ---- Wait until dashboard loads ----
        self.page.wait_for_url(DASHBOARD_URL)
        self.page.wait_for_timeout(1000)
