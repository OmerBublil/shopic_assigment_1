import os
import json
import logging
from UploadPage import UploadPage

logger = logging.getLogger(__name__)


class csv_upload_tester:
    def __init__(self, csv_path, expected_key, expected_status):
        """
        Initializes the tester with path to CSV file, expected key in the JSON,
        and the expected result status (success or error).
        """
        self.csv_path = csv_path
        self.expected_key = expected_key
        self.expected_status = expected_status
        self.base_url = os.getenv("APP_URL", "http://localhost:8000")
        logger.info(
            f"Initialized tester with CSV: {csv_path}, expected_status: {expected_status}")


    def extract_error_rows(self, error_messages):
        """
        Extracts row numbers from error messages that mention 'row'.
        Used to count how many specific rows failed.
        """
        error_rows = []
        for error in error_messages:
            if isinstance(error, str):
                if "row" in error:
                    try:
                        row_num = int(error.split("row")[1].strip().split()[0])
                        error_rows.append(row_num)
                    except Exception:
                        continue
        return error_rows


    def run(self, page):
        """
        Main test logic: uploads the file, collects the result from the site,
        compares with expected results, and raises assertion if mismatch is found.
        """
        upload_page = UploadPage(page)
        upload_page.navigate(self.base_url)
        logger.info(f"Navigated to {self.base_url}")

        # Before attempting to upload the file
        if not os.path.exists(self.csv_path):
            logger.error(f"CSV file not found: {self.csv_path}. Aborting upload.")
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        upload_page.upload_file(self.csv_path)
        logger.info(f"Uploaded file: {self.csv_path}")

        upload_page.submit()
        logger.info("Submitted the form")

        # Get the base path of the project (root folder)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        EXPECTED_RESULTS_PATH = os.path.join(BASE_DIR, "data", "expected_results.json")

        try:
            result_json = upload_page.get_results()
        except Exception as e:
            logging.error(f"Exception while getting results: {e}")
            result_json = {"status": "error", "message": f"Unexpected error while parsing result: {e}"}

        try:
            logger.info("Loading expected results from JSON file")
            with open(EXPECTED_RESULTS_PATH) as f:
                expected_results = json.load(f)
            expected = expected_results[self.expected_key]
            logger.info(f"Loaded expectations for key '{self.expected_key}'")
        except FileNotFoundError:
            logger.error("Expected results file not found.")
            raise
        except KeyError:
            logger.error(f"Key '{self.expected_key}' not found in expected results file.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON file: {e}")
            raise


        # Extract expected values
        total_expected = expected["total"]
        success_expected = expected["success_count"]
        error_expected = expected["error_count"]
        expected_errors = expected.get("expected_errors", [])

        # Parse actual results
        actual_success_count = len(result_json.get("data", [])) if "data" in result_json else 0
        logger.info(f"Actual success count: {actual_success_count}")

        failures = []

        # Extract errors from response
        actual_errors = result_json.get("errors")
        if not actual_errors or not isinstance(actual_errors, list):
            actual_errors = []

        # If no structured errors, fall back to error message string
        if not actual_errors and "message" in result_json:
            logger.info("No 'errors' field found, falling back to 'message' field")
            actual_errors = [result_json["message"]]

        # Ensure errors exist when error is expected
        if self.expected_status == "error" and not actual_errors:
            logger.warning("Expected error status but no errors or message were returned in response")
            failures.append("Expected error status but no errors or message were returned in response")

        actual_error_rows_count = len(self.extract_error_rows(actual_errors))
        logger.info(f"Actual error rows count: {actual_error_rows_count}")

        actual_total = actual_success_count + actual_error_rows_count
        logger.info(f"Computed total rows (successes + errors): {actual_total}")

        # Compare actual results to expected
        logger.info(f"Checking response status: expected '{self.expected_status}', got '{result_json['status']}'")
        if result_json["status"] != self.expected_status:
            failures.append(f"Expected status '{self.expected_status}', got '{result_json['status']}'")

        logger.info(f"Checking success count: expected {success_expected}, got {actual_success_count}")
        if actual_success_count != success_expected:
            failures.append(f"Expected {success_expected} successes, got {actual_success_count}")

        logger.info(f"Checking error count: expected {error_expected}, got {actual_error_rows_count}")
        if actual_error_rows_count != error_expected:
            failures.append(f"Expected {error_expected} errors, got {actual_error_rows_count}")

        logger.info(f"Checking total records: expected {total_expected}, got {actual_total}")
        if actual_total != total_expected:
            failures.append(f"Expected total {total_expected}, got {actual_total}")

        logger.info(f"Expected errors: {expected_errors}")
        logger.info(f"Actual errors: {actual_errors}")

        # Detect missing or extra errors
        missing = [e for e in expected_errors if e not in actual_errors]
        unexpected = [e for e in actual_errors if e not in expected_errors]

        if missing:
            logger.warning(f"Missing expected errors: {missing}")
            failures.append(f"Missing expected errors: {missing}")

        if unexpected:
            logger.warning(f"Unexpected errors found: {unexpected}")
            failures.append(f"Unexpected errors found: {unexpected}")

        # Final assertion if any failure detected
        if failures:
            full_message = "\n".join(failures)
            separator = "\n" + "=" * 60 + "\n"
            logger.error(f"Test failed with the following issues:\n{full_message}")
            assert False, f"{separator}Test failed with the following issues:\n{full_message}{separator}"
        else:
            logger.info("Test passed successfully.")

