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

import datetime
import logging
from dataclasses import dataclass
from http.client import responses
from typing import Tuple, TypeVar

from ethtx import exceptions as ethtx_exceptions
from flask import Blueprint, request
from web3.exceptions import TransactionNotFound
from werkzeug.exceptions import HTTPException

from .utils import as_dict
from ..exceptions import *

log = logging.getLogger(__name__)

exceptions_bp = Blueprint("exceptions", __name__)


@as_dict
@dataclass
class BaseRequestException:
    """Base Request Exception"""

    status: int
    error: str
    path: str
    message: str = ""
    timestamp: datetime.datetime.utcnow = None

    def __post_init__(self):
        """Post init values."""
        self.error = str(self.error)
        self.message = responses[self.status]
        self.timestamp = datetime.datetime.utcnow()


BaseErrorType = TypeVar("BaseErrorType", bound=Tuple[BaseRequestException, int])


@exceptions_bp.app_errorhandler(HTTPException)
def handle_all_http_exceptions(error: HTTPException) -> BaseErrorType:
    """All HTTP Exceptions handler."""
    return BaseRequestException(error.code, error.description, request.path), error.code


@exceptions_bp.app_errorhandler(ethtx_exceptions.NodeConnectionException)
def node_connection_error(error) -> BaseErrorType:
    """EthTx - Node connection error."""
    return BaseRequestException(500, error, request.path), 500


@exceptions_bp.app_errorhandler(ethtx_exceptions.ProcessingException)
def processing_error(error) -> BaseErrorType:
    """EthTx - Processing error."""
    return BaseRequestException(500, error, request.path), 500


@exceptions_bp.app_errorhandler(ethtx_exceptions.InvalidTransactionHash)
def invalid_transaction_hash(error) -> BaseErrorType:
    """EthTx - Invalid transaction hash."""
    return BaseRequestException(400, error, request.path), 400


@exceptions_bp.app_errorhandler(TransactionNotFound)
def transaction_not_found(error) -> BaseErrorType:
    """Could not find transaction."""
    return BaseRequestException(404, error, request.path), 404


@exceptions_bp.app_errorhandler(AuthorizationError)
def authorization_error(error) -> BaseErrorType:
    """Unauthorized request."""
    return BaseRequestException(401, error, request.path), 401


@exceptions_bp.app_errorhandler(MalformedRequest)
def malformed_request(error) -> BaseErrorType:
    """Wrong request."""
    return BaseRequestException(400, error, request.path), 400


@exceptions_bp.app_errorhandler(PayloadTooLarge)
def payload_too_large(error) -> BaseErrorType:
    """Payload is too large."""
    return BaseRequestException(413, error, request.path), 413


@exceptions_bp.app_errorhandler(ResourceLockedError)
def resource_locked_error(error) -> BaseErrorType:
    """Resource is locked."""
    return BaseRequestException(423, error, request.path), 423


@exceptions_bp.app_errorhandler(Exception)
def unexpected_error(error) -> BaseErrorType:
    """Unexpected error."""
    log.exception(str(error))

    return BaseRequestException(500, str(UnexpectedError()), request.path), 500
