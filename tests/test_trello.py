import os
import pytest
import logging
from dotenv import load_dotenv  # type: ignore
from playwright.sync_api import sync_playwright

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class TrelloLoginPage:
    def __init__(self, page):
        self.page = page

    def login_with_google(self, email, password):
        logger.info("Clicking Google login button")
        self.page.click('#google-auth-button')

        # Check for "Use another account" option and click it if necessary
        if self.page.is_visible('text="Use another account"', timeout=10000):
            logger.info("Clicking 'Use another account'")
            self.page.click('text="Use another account"')

        logger.info("Filling in the Google email and clicking Next")
        self.page.fill('input[type="email"]', email)
        self.page.click('button:has-text("Next")')

        # Wait for the password field, enter password, and click Next
        self.page.wait_for_selector('input[type="password"]', timeout=10000)
        logger.info("Filling in the Google password and clicking Next")
        self.page.fill('input[type="password"]', password)
        self.page.click('button:has-text("Next")')

    def is_logged_in(self):
        # Wait for the Trello home link to ensure the user is logged in
        logger.info("Waiting for the home link after login")
        return self.page.is_visible("a[data-test-id='home-link']")


@pytest.fixture(scope="function")
def playwright_setup():
    # Set the headless mode based on the environment variable
    headless = False
    logger.info("Launching Firefox ")

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


def test_login_to_trello_with_google(playwright_setup):
    # Credentials from environment variables
    google_email = os.getenv("GOOGLE_EMAIL")
    google_password = os.getenv("GOOGLE_PASSWORD")

    # Check if the credentials are loaded properly
    if not google_email or not google_password:
        logger.error("Please set GOOGLE_EMAIL and GOOGLE_PASSWORD.")
        pytest.fail("Google credentials are missing.")

    page = playwright_setup
    trello_login_page = TrelloLoginPage(page)

    logger.info("Navigating to Trello login page")
    page.goto("https://trello.com/login")

    # Perform login
    trello_login_page.login_with_google(google_email, google_password)

    # Assert that login is successful
    assert trello_login_page.is_logged_in(), "Login failed!"
    logger.info("Login test passed.")
