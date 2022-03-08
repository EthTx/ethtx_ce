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

import os

from dotenv import load_dotenv, find_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(find_dotenv(filename="../../.env"))


class Config:
    """Base Config."""

    LOGGING_CONFIG = os.environ.get(
        "LOGGING_CONFIG", os.path.join(BASE_DIR, "../log_cfg.json")
    )
    LOGGING_LOG_PATH = os.environ.get(
        "LOGGING_CONFIG", os.path.join(BASE_DIR, "../../tmp")
    )

    API_KEY = os.getenv("API_KEY", "")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    ETHTX_ADMIN_USERNAME = os.getenv("ETHTX_ADMIN_USERNAME")
    ETHTX_ADMIN_PASSWORD = os.getenv("ETHTX_ADMIN_PASSWORD")


class ProductionConfig(Config):
    """Production Config."""

    ENV = "production"
    FLASK_DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class StagingConfig(Config):
    """Staging Config."""

    ENV = "staging"
    FLASK_DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    """Development Config."""

    ENV = "development"
    FLASK_DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
