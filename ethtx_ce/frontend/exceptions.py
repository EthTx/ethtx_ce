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

import logging
from functools import wraps
from typing import Callable, Optional

from ethtx import exceptions as ethtx_exceptions
from flask import Blueprint, render_template
from web3.exceptions import TransactionNotFound
from werkzeug.exceptions import HTTPException

from .deps import extract_tx_hash_from_req
from ..exceptions import *

log = logging.getLogger(__name__)

exceptions_bp = Blueprint("exceptions", __name__)


def render_error_page(status: Optional[int] = 500):
    """Render error page."""

    def _render_error_page(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            error = f(*args, **kwargs)
            status_code = status
            if isinstance(error, HTTPException):
                error, status_code = error.description, error.code
            return (
                render_template(
                    "exception.html",
                    status_code=status_code,
                    error=error,
                    tx_hash=extract_tx_hash_from_req(),
                ),
                status_code,
            )

        return wrapper

    return _render_error_page


@exceptions_bp.app_errorhandler(HTTPException)
@render_error_page()
def handle_all_http_exceptions(error: HTTPException) -> HTTPException:
    """All HTTP Exceptions handler."""
    return error


@exceptions_bp.app_errorhandler(ethtx_exceptions.NodeConnectionException)
@render_error_page(500)
def node_connection_error(error) -> str:
    """EthTx - Node connection error."""
    return error


@exceptions_bp.app_errorhandler(ethtx_exceptions.ProcessingException)
@render_error_page(500)
def processing_error(error) -> str:
    """EthTx - Processing error."""
    return error


@exceptions_bp.app_errorhandler(ethtx_exceptions.InvalidTransactionHash)
@render_error_page(400)
def invalid_transaction_hash(error) -> str:
    """EthTx - Invalid transaction hash."""
    return error


@exceptions_bp.app_errorhandler(TransactionNotFound)
@render_error_page(404)
def transaction_not_found(error) -> str:
    """Could not find transaction."""
    return error


@exceptions_bp.app_errorhandler(AuthorizationError)
@render_error_page(401)
def authorization_error(error) -> str:
    """Unauthorized request."""
    return error


@exceptions_bp.app_errorhandler(MalformedRequest)
@render_error_page(400)
def malformed_request(error) -> str:
    """Wrong request."""
    return error


@exceptions_bp.app_errorhandler(PayloadTooLarge)
@render_error_page(413)
def payload_too_large(error) -> str:
    """Payload is too large."""
    return error


@exceptions_bp.app_errorhandler(ResourceLockedError)
@render_error_page(423)
def resource_locked_error(error) -> str:
    """Resource is locked."""
    return error


@exceptions_bp.app_errorhandler(EmptyResponseError)
@render_error_page(404)
def empty_response(error) -> str:
    """Response is empty."""
    return error


@exceptions_bp.app_errorhandler(Exception)
@render_error_page(500)
def unexpected_error(error) -> str:
    """Unexpected error."""
    log.exception(str(error))

    return str(UnexpectedError())
