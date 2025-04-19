import json
import logging

# Initialize a logger specific to this module
logger = logging.getLogger(__name__)

class UploadPage:
    """
    Page Object representing the CSV upload page.
    Encapsulates navigation, file upload, form submission, and result retrieval.
    """
    def __init__(self, page):
        """
        Initialize the UploadPage object with Playwright's page instance and define relevant UI elements.
        """
        self.page = page
        self.file_input = page.locator("input[type='file']")
        self.upload_button = page.locator("text=Upload")
        self.results_selector = "#results"

    def navigate(self, url):
        """
        Navigate to the given URL.
        """
        self.page.goto(url)

    def upload_file(self, file_path):
        """
        Upload a file to the file input field.
        """
        self.file_input.set_input_files(file_path)

    def submit(self):
        """
        Click the Upload button to trigger the file processing.
        """
        self.upload_button.click()

    def get_results(self):
        """
        Wait for the result container to appear and return the parsed JSON result.
        If the selector doesn't appear or parsing fails, return a structured error response.
        """
        try:
            self.page.wait_for_selector(self.results_selector, timeout=10000)
            raw = self.page.query_selector(self.results_selector).inner_text()
            return json.loads(raw)
        except TimeoutError:
            logger.error("Timeout: '#results' element did not appear within 10 seconds.")
            return {
                "status": "error",
                "errors": ["Timeout: No response received from the frontend."]
            }
        except Exception as e:
            logger.error(f"Exception while getting results: {e}")
            return {
                "status": "error",
                "errors": [f"Unexpected error while parsing result: {e}"]
            }

