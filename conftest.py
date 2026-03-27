import pytest
from playwright.sync_api import sync_playwright
from config import BASE_URL

# ----------------- Session-scoped Playwright -----------------
@pytest.fixture(scope="session")
def playwright_instance():
    """Start Playwright once per session."""
    with sync_playwright() as p:
        yield p

# ----------------- Session-scoped Browser -----------------
@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Launch browser once per session."""
    browser = playwright_instance.chromium.launch(
        headless=False,
        args=[
            "--use-fake-ui-for-media-stream",
            "--use-fake-device-for-media-stream",
            "--allow-file-access-from-files",
        ],
    )
    yield browser
    # Ensure browser closes at the end of the session
    try:
        browser.close()
    except Exception:
        pass

# ----------------- Function-scoped Page -----------------
@pytest.fixture
def page(browser):
    """Create new context and page per test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        locale="he-IL",
    )

    # Grant camera/microphone permissions explicitly
    context.grant_permissions(["camera", "microphone"], origin=BASE_URL)

    page = context.new_page()
    page.goto(BASE_URL)

    yield page

    # Ensure context closes safely even if test fails
    try:
        context.close()
    except Exception:
        pass