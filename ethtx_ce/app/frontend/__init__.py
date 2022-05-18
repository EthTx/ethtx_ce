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
from typing import Callable, Dict, Optional, Union, Type

from ethtx import EthTx
from flask import Blueprint, Flask


from .. import factory
from ..helpers import read_ethtx_versions


def create_app(
    engine: EthTx, settings_override: Optional[Union[Dict, Type]] = None
) -> Flask:
    """Returns Frontend app instance."""
    app = factory.create_app(
        __name__,
        __path__,
        settings_override,
        template_folder="frontend/templates",
        static_folder="frontend/static",
    )
    app.name = "ethtx_ce/frontend"

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.ethtx = engine  # init ethtx engine
    read_ethtx_versions(app)

    return app


def frontend_route(bp: Blueprint, *args, **kwargs):
    """Route in blueprint context."""

    def decorator(f: Callable):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        f.__name__ = str(id(f)) + f.__name__
        return f

    return decorator
