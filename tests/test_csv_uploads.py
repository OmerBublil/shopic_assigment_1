import pytest
from csv_upload_tester import csv_upload_tester
import os

# Build absolute paths to CSV files, relative to the root of the project.
# This allows test execution from the project root directory without path errors.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Define all test cases as (csv file path, key for expected results, expected status).
# These correspond to entries in expected_results.json
test_cases = [
    (os.path.join(DATA_DIR, "valid_products.csv"), "valid_products", "success"),
    (os.path.join(DATA_DIR, "invalid_products.csv"), "invalid_products", "error"),
    (os.path.join(DATA_DIR, "missing_price.csv"), "missing_price", "error"),
    (os.path.join(DATA_DIR, "empty_file.csv"), "empty_file", "error"),
    (os.path.join(DATA_DIR, "header_only.csv"), "header_only", "success"),
    (os.path.join(DATA_DIR, "non_numeric_price.csv"), "non_numeric_price", "error"),
    (os.path.join(DATA_DIR, "negative_price.csv"), "negative_price", "error"),
    (os.path.join(DATA_DIR, "missing_headers.csv"), "missing_headers", "error"),

    # Test case with non-existent file to verify error handling for missing CSVs.
    (os.path.join(DATA_DIR, "valid_productsss.csv"), "valid_products", "success"),
]

@pytest.mark.parametrize("csv_file, expected_key, expected_status", test_cases)
def test_csv_upload(csv_file, expected_key, expected_status, page):
    """
    Executes the CSV upload test for a given file, comparing actual results from the site
    against the expected results defined in expected_results.json.
    """
    tester = csv_upload_tester(csv_file, expected_key, expected_status)
    tester.run(page)
