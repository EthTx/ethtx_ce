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
from dataclasses import dataclass
from http.client import responses
from typing import Tuple

from flask import Blueprint, request
from web3.exceptions import TransactionNotFound

from ethtx_ce.backend.api.core.utils import as_dict
from ..exceptions import *

exceptions_bp = Blueprint("exceptions", __name__)


@as_dict
@dataclass
class BaseRequestException:
    """ Base Request Exception """

    status: int
    error: str
    path: str
    message: str = ""
    timestamp: datetime.datetime.utcnow = None

    def __post_init__(self):
        """ Post init values. """
        self.error = str(self.error)
        self.message = responses[self.status]
        self.timestamp = datetime.datetime.utcnow()


@exceptions_bp.app_errorhandler(InvalidTransactionHash)
def invalid_transaction_hash(error) -> Tuple[BaseRequestException, int]:
    """ Invalid transaction hash. """
    return BaseRequestException(400, error, request.path), 400


@exceptions_bp.app_errorhandler(Web3ConnectionException)
def web3_connection_error(error) -> Tuple[BaseRequestException, int]:
    """ Web3 connection problem. """
    return BaseRequestException(500, error, request.path), 500


@exceptions_bp.app_errorhandler(TransactionNotFound)
def transaction_not_found(error) -> Tuple[BaseRequestException, int]:
    """ Could not find transaction. """
    return BaseRequestException(404, error, request.path), 404


@exceptions_bp.app_errorhandler(AuthorizationError)
def authorization_error(error) -> Tuple[BaseRequestException, int]:
    """ Unauthorized request. """
    return BaseRequestException(401, error, request.path), 401


@exceptions_bp.app_errorhandler(MalformedRequest)
def malformed_request(error) -> Tuple[BaseRequestException, int]:
    """ Wrong request. """
    return BaseRequestException(400, error, request.path), 400


@exceptions_bp.app_errorhandler(PayloadTooLarge)
def payload_too_large(error) -> Tuple[BaseRequestException, int]:
    """ Payload is too large. """
    return BaseRequestException(413, error, request.path), 413


@exceptions_bp.app_errorhandler(MethodNotAllowed)
def method_not_allowed(error) -> Tuple[BaseRequestException, int]:
    """ Method is not allowed. """
    return BaseRequestException(405, error, request.path), 405


@exceptions_bp.app_errorhandler(ResourceLockedError)
def resource_locked_error(error) -> Tuple[BaseRequestException, int]:
    """ Resource is locked. """
    return BaseRequestException(423, error, request.path), 423


@exceptions_bp.app_errorhandler(UnexpectedError)
def unexpected_error(error) -> Tuple[BaseRequestException, int]:
    """ Unexpected error. """
    return BaseRequestException(500, error, request.path), 500


@exceptions_bp.app_errorhandler(InternalError)
def internal_error(error) -> Tuple[BaseRequestException, int]:
    """ Internal Error. """
    return BaseRequestException(500, error, request.path), 500
