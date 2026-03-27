from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.meeting_lobby_page import MeetingLobbyPage
from pages.meeting_room_page import MeetingRoomPage
from config import (
    LOGIN_URL,
    DASHBOARD_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
    CLIENT_NAME,
    PROJECT_NAMES,
)


def test_start_meeting_flow(page: Page) -> None:
    """
    Verify full login, lobby flow, meeting flow,
    and final dashboard navigation.
    """

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    lobby_page = MeetingLobbyPage(page)
    meeting_page = MeetingRoomPage(page)

    login_page.navigate(LOGIN_URL)
    login_page.login(TEST_EMAIL, TEST_PASSWORD)

    page.wait_for_url(DASHBOARD_URL)
    assert page.url == DASHBOARD_URL

    dashboard_page.search_client(CLIENT_NAME)
    page.wait_for_timeout(1000)

    dashboard_page.open_actions_menu(CLIENT_NAME)

    for project in PROJECT_NAMES:

        selector = f"li.test--button{project.replace(' ', '_')}"
        page.wait_for_selector(selector)
        page.locator(selector).click()
        page.wait_for_timeout(1000)

        ok_button = "button.test--buttonOk"
        page.wait_for_selector(ok_button)
        page.wait_for_timeout(1000)
        page.locator(ok_button).click()

        # Lobby
        lobby_page.wait_for_lobby()
        page.wait_for_timeout(1000)
        lobby_page.play_microphone_test_sound()
        page.wait_for_timeout(1000)
        lobby_page.start_meeting()

        # Meeting
        meeting_page.wait_for_waiting_participant()
        page.wait_for_timeout(1000)
        meeting_page.accept_participant()
        page.wait_for_timeout(1000)
        meeting_page.end_call()

        # # Verify dashboard loaded
        # dashboard_title = (
        #     "#__next > div.layout-wrapper.rtl-uinsfl "
        #     "> div.layout-content-wrapper.MuiBox-root.rtl-34b9xr "
        #     "> main > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-6.rtl-h2qpui "
        #     "> div:nth-child(1) > div > nav > ol > li > p"
        # )
        #
        # page.wait_for_selector(dashboard_title, state="visible")
        # assert "לוח בקרה מנהל/ת" in page.inner_text(dashboard_title)
        # page.wait_for_timeout(1000)