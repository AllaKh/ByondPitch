from pages.base_page import BasePage
import time
from playwright.sync_api import Page

class LoginPage(BasePage):
    """
    Page Object for the login page.
    Supports email entry, password entry, and error message retrieval.
    """

    # --- Selectors ---
    EMAIL_INPUT = "#\\:r1\\:-label"
    PASSWORD_INPUT = "#__next > div.layout-wrapper.MuiBox-root.rtl-cipdl > div > div > div.MuiBox-root.rtl-1pivp1q > div > div > form > div.MuiFormControl-root.MuiFormControl-fullWidth.rtl-m5bgtg > div > input"
    LOGIN_BUTTON = "#\\:r2\\:"
    ERROR_MESSAGE = "#__next > div.layout-wrapper.MuiBox-root.rtl-cipdl > div > div > div.MuiBox-root.rtl-1pivp1q > div > div > form > div.MuiFormControl-root.MuiFormControl-fullWidth.rtl-m5bgtg > p"

    def __init__(self, page: Page):
        super().__init__(page)

    # --- Step 1: Email ---
    def login_with_email_only(self, email: str) -> None:
        """
        Fill in the email field and click login to proceed to password step.
        """
        self.fill(self.EMAIL_INPUT, email)
        self.click(self.LOGIN_BUTTON)

    # --- Step 2: Password ---
    def login_with_password(self, password: str) -> None:
        """
        Fill in the password field and click login.
        Includes a 1-second delay after submission.
        """
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        time.sleep(1)

    # --- Check if email is displayed ---
    def is_email_visible(self, email: str) -> bool:
        """
        Returns True if the email appears on the page after the first step.
        """
        return self.page.locator(f"text={email}").is_visible()

    # --- Retrieve error text ---
    def get_error_text(self) -> str:
        """
        Returns the text content of the error message element.
        """
        return self.page.locator(self.ERROR_MESSAGE).inner_text()