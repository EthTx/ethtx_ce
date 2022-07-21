# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

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
