import subprocess
import os
import logging


class TestRunner:
    """
    Executes test cases for Mabel.
    """

    def __init__(self, test_dir="tests"):
        self.test_dir = test_dir
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def run_unit_tests(self):
        """
        Run unit tests in the tests/unit directory.
        """
        self.logger.info("Running unit tests...")
        result = subprocess.run(["pytest", os.path.join(self.test_dir, "unit")], capture_output=True, text=True)
        self.logger.info(result.stdout)
        self.logger.error(result.stderr)

    def run_integration_tests(self):
        """
        Run integration tests in the tests/integration directory.
        """
        self.logger.info("Running integration tests...")
        result = subprocess.run(["pytest", os.path.join(self.test_dir, "integration")], capture_output=True, text=True)
        self.logger.info(result.stdout)
        self.logger.error(result.stderr)

    def run_all_tests(self):
        """
        Run all tests (unit and integration).
        """
        self.logger.info("Starting all tests...")
        self.run_unit_tests()
        self.run_integration_tests()


if __name__ == "__main__":
    runner = TestRunner()
    runner.run_all_tests()
