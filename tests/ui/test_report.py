import json
import logging
import sys
from pathlib import Path
import logging
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
import curly_octo_guacamole.ui.framework.utils as utils
import pytest


def test_generate_report(test_data, report_json, log):
    log.info("Testing Generating report...")
    log.info("Testing report data: %s", test_data)
    utils.generate_report()
    with open("report.json", "r") as file:
        report_data = json.load(file)
    log.info("Loaded report data: %s", report_data)
    assert type(report_data) == dict, "Report data should be a dictionary"
    assert report_data == test_data, "Report data does not match expected data"

def test_report_fields(report_json, log):
    log.info("Testing report fields...")
    log.info("Loaded report data: %s", report_json)
    assert "timestamp" in report_json, "Timestamp field is missing in report"
    assert "test_name" in report_json, "Test name field is missing in report"
    assert "status" in report_json, "Status field is missing in report"
    assert "details" in report_json, "Details field is missing in report"
    assert isinstance(report_json["details"], dict), "Details should be a dictionary"

@pytest.fixture(scope="session")
def log():

    """Fixture to set up logging for the tests."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

@pytest.fixture(scope="session")
def test_data():

    """Fixture to provide test data for report generation."""
    
    return {
        "timestamp": "2023-10-01T12:00:00Z",
        "test_name": "Test Report Generation",
        "status": "success",
        "details": {
            "passed": 10,
            "failed": 2,
            "skipped": 1,
            "total": 13,
        },
    }

@pytest.fixture(scope="session")
def report_json():

    """Fixture to load report data from a JSON file."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Getting report data via test fixture...")

    with open("report.json", "r") as file:
        report_data = json.load(file)
        logger.info("Loaded report data: %s", report_data)
        return report_data

# pdm run pytest tests/ui/test_report.py --log-cli-level=INFO    
    