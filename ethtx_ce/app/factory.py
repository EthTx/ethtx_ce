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
from typing import Optional, Dict

from flask import Flask

from .config import Config
from .helpers import class_import, register_blueprints
from .logger import setup_logging

env = os.getenv("ENV", "development").capitalize()
config_class = f"app.config.{env}Config"
config: Config = class_import(config_class)


def create_app(
    package_name: str,
    package_path: str,
    settings_override: Optional[Dict] = None,
    **app_kwargs,
) -> Flask:
    """
    Returns a :class:`Flask` application instance
    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param app_kwargs: additional app kwargs
    """
    app = Flask(__name__, instance_relative_config=True, **app_kwargs)

    app.config.from_object(config)
    setup_logging(app=app)
    app.config.from_object(settings_override)

    register_blueprints(app, package_name, package_path)

    return app
