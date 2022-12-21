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

import logging
from functools import wraps
from typing import Callable, Optional

import jsonpickle
from flask import request, current_app, jsonify

from ..exceptions import (
    AuthorizationError,
    PayloadTooLarge,
    UnexpectedError,
    InternalError,
)
from .utils import enable_direct, delete_bstrings

log = logging.getLogger(__name__)

jsonpickle.set_decoder_options('simplejson', use_decimal=True)


def auth_required(func: Callable):
    """api key  verification."""

    @wraps(func)
    def check_auth(**kwargs):
        api_key = request.headers.get("x-api-key") or request.args.get("api_key")
        if api_key != current_app.config.get("API_KEY"):
            raise AuthorizationError(api_key)

        return func(**kwargs)

    return check_auth


def response(status: Optional[int] = 200):
    """
    Return response with:
    :param status: response status code, default: `200`
    """

    def _response(f: Callable):
        @wraps(f)
        def wrapped(*args, **kwargs):
            func = f(*args, **kwargs)

            try:
                data = jsonify(
                    delete_bstrings(
                        jsonpickle.decode(
                            jsonpickle.encode(func, make_refs=False, unpicklable=False, use_decimal=True)
                        )
                    )
                )
            except TypeError as e:
                log.critical("Response cannot be serialized. %s", e)
                raise InternalError()
            except Exception as e:
                log.exception(e)
                raise UnexpectedError()

            return data, status

        return wrapped

    return _response


@enable_direct
def limit_content_length(max_length: Optional[int] = None):
    """
    Limit content length. If not given:
    The priority has app MAX_CONTENT_LENGTH value.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            app_max_length = current_app.config.get("MAX_CONTENT_LENGTH")
            max_content_length = max_length if max_length else app_max_length

            if cl is not None and cl > max_content_length:
                raise PayloadTooLarge(
                    content_length=cl, max_content_length=max_content_length
                )
            return f(*args, **kwargs)

        return wrapper

    return decorator
