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
import secrets

from dotenv import load_dotenv, find_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(find_dotenv(filename="../.env"))


class SwaggerConfig:
    """Swagger ui basic config."""

    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get", "post"]


class EthConfig:
    """EthTx useful parameters."""

    NODES_WITH_URLS = {
        "mainnet": os.getenv("MAINNET_NODE_URL", ""),
        "kovan": os.getenv("KOVAN_NODE_URL", ""),
        "ropsten": os.getenv("ROPSTEN_NODE_URL", ""),
        "optimism": os.getenv("OPTIMISM_NODE_URL", ""),
    }
    DEFAULT_CHAIN = "mainnet"
    ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY", "")


class Config(SwaggerConfig):
    """Base Config."""

    LOGGING_CONFIG = os.environ.get(
        "LOGGING_CONFIG", os.path.join(BASE_DIR, "../log_cfg.json")
    )
    LOGGING_LOG_PATH = os.environ.get(
        "LOGGING_CONFIG", os.path.join(BASE_DIR, "../tmp")
    )

    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))
    API_KEY = os.getenv("API_KEY", "")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "")
    MONGODB_DB = os.getenv("MONGODB_DB", "")

    # to be deleted mongo parameters
    MONGODB_HOST = os.getenv("MONGODB_HOST", "")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")

    ETHTX_ADMIN_USERNAME = os.getenv("ETHTX_ADMIN_USERNAME")
    ETHTX_ADMIN_PASSWORD = os.getenv("ETHTX_ADMIN_PASSWORD")


class ProductionConfig(Config):
    """Production Config."""

    ENV = "production"
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class StagingConfig(Config):
    """Staging Config."""

    ENV = "staging"
    DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    """Development Config."""

    ENV = "development"
    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
