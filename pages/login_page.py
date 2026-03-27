import json
import random
from playwright.sync_api import Page
from pages.base_page import BasePage
from config import LANGUAGE
from error_messages import get_error


class LoginPage(BasePage):
    """
    Page Object Model for the Login page.
    Encapsulates login actions and invalid password validation logic.
    """

    EMAIL_INPUT = "#\\:r1\\:-label"
    PASSWORD_INPUT = "#__next > div.layout-wrapper.MuiBox-root.rtl-cipdl > div > div > div.MuiBox-root.rtl-1pivp1q > div > div > form > div.MuiFormControl-root.MuiFormControl-fullWidth.rtl-m5bgtg > div > input"
    LOGIN_BUTTON = "#\\:r2\\:"
    ERROR_MESSAGE = "#__next > div.layout-wrapper.MuiBox-root.rtl-cipdl > div > div > div.MuiBox-root.rtl-1pivp1q > div > div > form > div.MuiFormControl-root.MuiFormControl-fullWidth.rtl-m5bgtg > p"

    def __init__(self, page: Page):
        super().__init__(page)

    def login(self, email: str, password: str) -> None:
        """
        Perform full login with email and password.
        """
        self.wait_visible(self.EMAIL_INPUT)
        self.fill(self.EMAIL_INPUT, email)
        self.click(self.LOGIN_BUTTON)

        self.wait_visible(self.PASSWORD_INPUT)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

        self.page.wait_for_load_state("networkidle")

    def login_with_email_only(self, email: str) -> None:
        """
        Enter email and proceed to password step.
        """
        self.wait_visible(self.EMAIL_INPUT)
        self.fill(self.EMAIL_INPUT, email)
        self.click(self.LOGIN_BUTTON)
        self.wait_visible(self.PASSWORD_INPUT)

    def login_with_password(self, password: str) -> None:
        """
        Enter password and submit login.
        """
        self.wait_visible(self.PASSWORD_INPUT)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_email_visible(self, email: str) -> bool:
        """
        Check whether the email is visible on the page.
        """
        return self.page.locator(f"text={email}").is_visible()

    def get_error_text(self) -> str:
        """
        Retrieve the current error message text.
        """
        self.wait_visible(self.ERROR_MESSAGE)
        return self.page.locator(self.ERROR_MESSAGE).inner_text()

    def attempt_invalid_passwords_until_limit(
        self,
    ) -> tuple[int, bool, int | None]:
        """
        Attempt all invalid passwords in randomized order
        until rate limit error is triggered.

        Returns:
            attempts (int): number of attempts performed
            limit_triggered (bool): whether rate limit was triggered
            limit_triggered_at (int | None): attempt number when limit triggered
        """

        with open("invalid_passwords.json", "r", encoding="utf-8") as f:
            payload = json.load(f)

        passwords = payload.get("invalidPasswords", [])
        random.shuffle(passwords)

        invalid_error = get_error(LANGUAGE, "invalid_credentials")
        limit_error = get_error(LANGUAGE, "attempts_exceeded")

        attempts = 0
        limit_triggered = False
        limit_triggered_at = None

        for pwd in passwords:
            self.fill(self.PASSWORD_INPUT, "")
            self.login_with_password(pwd)

            self.page.wait_for_selector(self.ERROR_MESSAGE, timeout=3000)
            error_text = self.get_error_text()

            attempts += 1
            print(f"Attempt {attempts}: '{pwd}' → {error_text}")

            if invalid_error in error_text:
                continue

            if limit_error in error_text:
                limit_triggered = True
                limit_triggered_at = attempts
                break

            raise AssertionError(f"Unexpected error message: {error_text}")

        return attempts, limit_triggered, limit_triggered_at