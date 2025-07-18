import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
import curly_octo_guacamole.ui.framework.utils as utils
import pytest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_root():
    """Test the root function from utils module."""

    logger.info("Testing root function with various inputs...")
    assert utils.root(4) == 2
    assert utils.root(9) == 3
    assert utils.root(16) == 4
    assert utils.root(25) == 5
    assert utils.root(0) == 0
    assert utils.root(1) == 1
    assert utils.root(-1) == pytest.approx(complex(0, 1))  # Complex result for negative input

# pdm run pytest --version
# pdm run pytest tests/ui/test_utils.py
# Enable print statements in pytest
# pdm run pytest tests/ui/test_utils.py -s
# Enable logging in pytest
# pdm run pytest tests/ui/test_utils.py -s --log-cli-level=INFO
# pdm run pytest tests/ui/test_utils.py -v
# pdm run pytest tests/ui/test_utils.py -v --tb=short
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root"
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO --no-cov-on-fail
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO --no-cov-on-fail
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO --no-cov-on-fail --strict-markers
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO --no-cov-on-fail --strict-markers
# pdm run pytest tests/ui/test_utils.py -v --tb=short --disable-warnings -k "test_root" --maxfail=1 --capture=no --show-capture=all --junitxml=reports/test-utils.xml --html=reports/test-utils.html --self-contained-html --cov=src/curly_octo_guacamole/ui/framework/utils.py --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=80 --durations=10 --log-cli-level=INFO --no-cov-on-fail --strict-markers --showlocals