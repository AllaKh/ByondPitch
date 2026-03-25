import json
import random
from playwright.sync_api import Page
from pages.login_page import LoginPage
from config import TEST_EMAIL, LANGUAGE
from error_messages import get_error

def test_login_invalid_passwords(page: Page) -> None:
    """
    Test invalid login attempts for maximum coverage.
    Randomizes password order and verifies:
      1. Invalid credentials message for each attempt
      2. Rate limit error appears if maximum attempts exceeded
    """

    login = LoginPage(page)
    page.wait_for_load_state("domcontentloaded")

    # Step 1 — enter email
    login.login_with_email_only(TEST_EMAIL)
    page.wait_for_timeout(1000)  # delay after email step
    page.wait_for_selector(f"text={TEST_EMAIL}", timeout=3000)
    assert login.is_email_visible(TEST_EMAIL), "Email not visible after first step"

    # Load passwords
    with open("invalid_passwords.json", "r", encoding="utf-8") as f:
        payload = json.load(f)

    passwords = payload.get("invalidPasswords", [])
    random.shuffle(passwords)  # randomize order each run

    invalid_error = get_error(LANGUAGE, "invalid_credentials")
    limit_error = get_error(LANGUAGE, "attempts_exceeded")

    attempts = 0
    limit_triggered = False
    limit_triggered_at = None

    for pwd in passwords:
        login.fill(login.PASSWORD_INPUT, "")
        login.login_with_password(pwd)  # includes 1s delay

        page.wait_for_selector(login.ERROR_MESSAGE, timeout=3000)
        error_text = login.get_error_text()

        attempts += 1
        print(f"Attempt {attempts}: '{pwd}' → {error_text}")

        if invalid_error in error_text:
            continue

        if limit_error in error_text:
            limit_triggered = True
            limit_triggered_at = attempts
            break

        assert False, f"Unexpected error message: {error_text}"

    # Validate that rate limit was triggered
    assert limit_triggered, f"Rate limit was NOT triggered after {attempts} attempts"
    print(f"Rate limit triggered at attempt: {limit_triggered_at}")