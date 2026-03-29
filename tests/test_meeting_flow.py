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
    Test full meeting flow:
    - login
    - search client
    - open first project only
    - start meeting
    - accept participant
    - end call and fill follow-up task
    - click finish task and check dashboard URL
    """

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    lobby_page = MeetingLobbyPage(page)
    meeting_page = MeetingRoomPage(page)

    # Login
    login_page.navigate(LOGIN_URL)
    login_page.login(TEST_EMAIL, TEST_PASSWORD)

    page.wait_for_url(DASHBOARD_URL)
    assert page.url == DASHBOARD_URL

    # Search client and open actions menu
    dashboard_page.search_client(CLIENT_NAME)
    dashboard_page.open_actions_menu(CLIENT_NAME)

    # --- Only choose the first project ---
    first_project = PROJECT_NAMES[0]
    selector = f"li.test--button{first_project.replace(' ', '_')}"
    page.wait_for_selector(selector)
    page.locator(selector).click()

    ok_button = "button.test--buttonOk"
    page.wait_for_selector(ok_button)
    page.locator(ok_button).click()

    # Lobby actions
    lobby_page.wait_for_lobby()
    lobby_page.play_microphone_test_sound()
    lobby_page.start_meeting()

    # Meeting room actions
    meeting_page.wait_for_waiting_participant()
    meeting_page.accept_participant()

    # End call and fill follow-up
    meeting_page.end_call()
    assert page.url == DASHBOARD_URL