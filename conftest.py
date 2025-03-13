import pytest
import logging
import os
from datetime import datetime
from core import ROOT_WORKING_DIRECTORY, LOGS_FOLDER


def pytest_configure():
    """Setup pytest logging globally before tests start."""
    log_dir = os.path.join(ROOT_WORKING_DIRECTORY, LOGS_FOLDER)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, datetime.now().strftime("%d_%m_%Y_%H_%M_%S.log"))

    logger = logging.getLogger("pytest-logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    pytest.logger = logger
