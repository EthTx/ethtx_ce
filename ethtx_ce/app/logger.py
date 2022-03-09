#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import logging
import logging.config
import os

from flask import Flask


def setup_logging(app: Flask):
    """Setup logging"""
    with open(app.config["LOGGING_CONFIG"], "r") as f:
        config = json.load(f)

    config["root"]["level"] = "DEBUG" if app.config["DEBUG"] else "INFO"
    filename = config["handlers"]["file_handler"]["filename"]
    if "/" not in filename:
        log_file_path = os.path.join(app.config["LOGGING_LOG_PATH"], filename)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        config["handlers"]["file_handler"]["filename"] = log_file_path

    logging.config.dictConfig(config)

    setup_external_logging()


def setup_external_logging() -> None:
    """Setup and override external libs loggers."""
    logging.getLogger("web3").setLevel(logging.INFO)  # web3 logger
