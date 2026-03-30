from playwright.sync_api import Page
from pages.login_page import LoginPage
from config import TEST_EMAIL


def test_login_invalid_passwords(page: Page) -> None:
    """
    Validate invalid login attempts and ensure
    rate limit error is triggered.
    """

    login = LoginPage(page)
    page.wait_for_load_state("domcontentloaded")

    login.login_with_email_only(TEST_EMAIL)
    page.wait_for_timeout(1000)
    page.wait_for_selector(f"text={TEST_EMAIL}", timeout=2000)

    assert login.is_email_visible(TEST_EMAIL)

    attempts, limit_triggered, limit_triggered_at = (
        login.attempt_invalid_passwords_until_limit()
    )

    assert limit_triggered, (
        f"Rate limit was NOT triggered after {attempts} attempts"
    )

    print(f"Rate limit triggered at attempt: {limit_triggered_at}")