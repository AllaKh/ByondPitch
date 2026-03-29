import json
from playwright.sync_api import Page
from pages.base_page import BasePage
from datetime import datetime
from config import DASHBOARD_URL


class MeetingRoomPage(BasePage):

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

    def _detect_language(self) -> str:
        self.page.wait_for_load_state("domcontentloaded")
        html_lang = self.page.locator("html").get_attribute("lang")
        if not html_lang:
            return "ENG"
        lang = html_lang.lower()
        if "he" in lang:
            return "HE"
        if "ru" in lang:
            return "RU"
        return "ENG"

    def _load_translations(self) -> dict:
        with open("languages.json", encoding="utf-8") as f:
            data = json.load(f)
        return data[self._detect_language()]

    def wait_for_waiting_participant(self) -> None:
        self.wait_visible(self.WAITING_PARTICIPANT_TITLE)

    def accept_participant(self) -> None:
        self.page.locator(self.ACCEPT_PARTICIPANT_BUTTON).first.click(force=True)
        self.page.wait_for_selector(self.CONFIRM_ACCEPT_BUTTON, state="visible")
        self.page.locator(self.CONFIRM_ACCEPT_BUTTON).click(force=True)
        self.page.wait_for_selector("div.MuiDialog-root", state="hidden")

    def end_call(self) -> None:
        translations = self._load_translations()
        self.page.wait_for_selector(self.END_CALL_BUTTON, state="visible")
        self.page.wait_for_timeout(3000)
        self.page.locator(self.END_CALL_BUTTON).last.click(force=True)
        self.page.wait_for_timeout(2000)

        self.page.wait_for_selector(self.WARNING_DIALOG, state="visible")
        warning_text = self.page.inner_text(self.WARNING_DIALOG)
        self.page.locator(self.WARNING_CONFIRM_BUTTON).click(force=True)
        self.page.wait_for_selector(self.WARNING_DIALOG, state="hidden")

        self.page.wait_for_selector(self.POST_CALL_DIALOG, state="visible")
        post_text = self.page.inner_text(self.POST_CALL_DIALOG)
        self.page.locator("div.MuiBox-root.rtl-1o9nvex button").click(force=True)
        self.page.wait_for_timeout(1500)

        subject_input = self.page.get_by_placeholder(translations["subject_placeholder"])
        subject_input.wait_for(state="visible")
        subject_input.fill(translations["subject"])

        dialog = self.page.locator("div.MuiDialog-root")
        description_input = dialog.get_by_label(translations["description_label"])
        description_input.wait_for(state="visible")
        description_input.fill(translations["description_primary"])

        now = datetime.now()
        formatted_now = f"{str(now.month).zfill(2)}/{str(now.day).zfill(2)}/{now.year} {str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}"

        date_input = dialog.get_by_placeholder(translations["datetime_placeholder"])
        date_input.wait_for(state="visible")
        date_input.fill(formatted_now)
        date_input.press("Enter")
        self.page.wait_for_timeout(1000)

        description_input_2 = dialog.locator("div.MuiFormControl-fullWidth input").nth(1)
        description_input_2.wait_for(state="visible")
        description_input_2.fill(translations["description_secondary"])

        self.page.locator("div.MuiDialogActions-root.rtl-10sjoy4 > button").click(force=True)
        dialog.wait_for(state="hidden")

        self.page.wait_for_timeout(2000)
        self.page.wait_for_url(DASHBOARD_URL)