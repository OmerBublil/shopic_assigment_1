# Shopic CSV Upload Automation Assignment

## Setup Instructions

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <shopic_assigment_1>
   cd shopic_assigment_1
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the local server before running any tests:
   ```bash
   python server/app.py
   ```

   **Note:** The server must be running locally at `http://localhost:8000` before test execution begins.

---

## Test Execution Instructions

Tests are written using `pytest` and `Playwright`.

To execute the tests:
```bash
pytest tests
```

To generate an HTML test report:
```bash
pytest tests/ --html=report.html
```

To create a plain text report:
```bash
pytest tests/ > test_report.txt
```

---

## Project Structure

```
shopic_assigment_1/
├── server/
│   └── app.py                     # Flask server that handles CSV uploads
├── tests/
│   ├── test_csv_uploads.py        # Automated test suite using Playwright and Pytest
│   ├── csv_upload_tester.py       # Core test logic and result validation
│   ├── UploadPage.py              # Page Object Model for interacting with the upload page
│   └── conftest.py                # Pytest fixtures for browser setup
├── data/
│   ├── valid_products.csv
│   ├── invalid_products.csv
│   ├── missing_price.csv
│   ├── empty_file.csv
│   ├── header_only.csv
│   ├── non_numeric_price.csv
│   ├── negative_price.csv
│   ├── missing_headers.csv
│   ├── empty_rows.csv
│   └── expected_results.json      # Expected output for each test case
├── report.html                    # HTML test execution report
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## Assumptions and Limitations

- The local server must be manually started before running the tests. It is assumed to be available at `http://localhost:8000`.
- All test CSV files are located in the `data/` directory.
- Expected results for each test case are defined in `expected_results.json`. The structure of this file must remain synchronized with the test inputs.
- Error messages returned by the application are matched as exact string values and are case-sensitive.
- Each CSV file is expected to include the following headers: `name`, `price`, `quantity`, and `category`.
- Files containing only headers or empty content are treated as edge cases and handled explicitly.
- If the server fails to respond within 10 seconds, the test will fail due to a timeout.
- No CI/CD pipeline is configured. All tests are executed manually.

---

## Test Report

A full test execution report is available in `report.html`.
