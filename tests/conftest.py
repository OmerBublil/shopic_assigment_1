import pytest
from playwright.sync_api import sync_playwright
import logging

# Configure logging to show INFO and above messages in a readable format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@pytest.fixture(scope="function")
def page():
    """
    Set up a new Playwright browser page for each test function and tear it down after the test finishes.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
