import subprocess
import os
import logging
import time


class Deployer:
    """
    Manages deployment processes for Mabel.
    """

    def __init__(self, app_dir="app", venv_dir="venv", requirements_file="requirements.txt"):
        self.app_dir = app_dir
        self.venv_dir = venv_dir
        self.requirements_file = requirements_file
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def create_virtual_environment(self):
        """
        Create a virtual environment.
        """
        self.logger.info("Creating virtual environment...")
        if not os.path.exists(self.venv_dir):
            subprocess.run(["python3", "-m", "venv", self.venv_dir])
            self.logger.info(f"Virtual environment created at {self.venv_dir}")
        else:
            self.logger.info("Virtual environment already exists.")

    def install_dependencies(self):
        """
        Install required Python packages.
        """
        self.logger.info("Installing dependencies...")
        subprocess.run([os.path.join(self.venv_dir, "bin", "pip"), "install", "-r", self.requirements_file])
        self.logger.info("Dependencies installed successfully.")

    def start_application(self):
        """
        Start the application using the virtual environment.
        """
        self.logger.info("Starting the application...")
        app_entry = os.path.join(self.app_dir, "main.py")
        if not os.path.exists(app_entry):
            self.logger.error(f"Application entry point {app_entry} not found.")
            return
        subprocess.run([os.path.join(self.venv_dir, "bin", "python"), app_entry])

    def deploy(self):
        """
        Full deployment process: environment creation, dependency installation, and app start.
        """
        self.create_virtual_environment()
        self.install_dependencies()
        self.start_application()


if __name__ == "__main__":
    deployer = Deployer()
    deployer.deploy()
