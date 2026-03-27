from playwright.sync_api import Page
from pages.base_page import BasePage


class MeetingLobbyPage(BasePage):
    """
    Page Object Model for Meeting Lobby (camera & mic check screen).
    """

    LOBBY_TITLE = "#__next > div.layout-wrapper.MuiBox-root.rtl-cipdl > div > div.MuiBox-root.rtl-1q1kcuq > div > h5"

    START_MEETING_BUTTON = "#__next > div.layout-wrapper.MuiBox-root.rtl-cipdl > div > div.MuiBox-root.rtl-1q1kcuq > div > div.MuiBox-root.rtl-1kaxbjd > button.test--pageMeetingLobby-buttonStartMeeting-stateEnabled"

    def __init__(self, page: Page):
        super().__init__(page)

    def wait_for_lobby(self) -> None:
        """
        Wait until lobby screen is visible.
        """
        self.wait_visible(self.LOBBY_TITLE)

    def play_microphone_test_sound(self) -> None:
        """
        Emit short beep to activate microphone test.
        """
        self.page.evaluate(
            """
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = ctx.createOscillator();
            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(440, ctx.currentTime);
            oscillator.connect(ctx.destination);
            oscillator.start();
            setTimeout(() => {
                oscillator.stop();
                ctx.close();
            }, 500);
            """
        )

    def start_meeting(self) -> None:
        """
        Click start meeting button.
        """
        self.wait_visible(self.START_MEETING_BUTTON)
        self.click(self.START_MEETING_BUTTON)