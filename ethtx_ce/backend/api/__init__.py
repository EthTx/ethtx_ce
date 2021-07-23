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
from typing import Callable

from flask import Blueprint

from .core.decorators import auth_required


def route(bp: Blueprint, *args, **kwargs):
    kwargs.setdefault("strict_slashes", False)

    def decorator(f: Callable):
        @bp.route(*args, **kwargs)
        @auth_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return rv, sc

        return f

    return decorator


# avoid circular
from .endpoints import *
from .exceptions import exceptions_bp
