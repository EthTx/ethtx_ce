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

from functools import wraps
from typing import Callable, Dict, Optional

from flask import Blueprint, Flask

from ethtx_ce import factory


def create_app(settings_override: Optional[Dict] = None) -> Flask:
    """Returns Frontend app instance. """
    app = factory.create_app(
        __name__,
        __path__,
        settings_override,
        template_folder="frontend/templates",
        static_folder="frontend/static",
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    return app


def route(bp: Blueprint, *args, **kwargs):
    """ Route in blueprint context. """

    def decorator(f: Callable):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator
