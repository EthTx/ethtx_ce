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

from typing import Optional, Union

__all__ = [
    "AuthorizationError",
    "MalformedRequest",
    "PayloadTooLarge",
    "MethodNotAllowed",
    "ResourceLockedError",
    "InternalError",
    "UnexpectedError",
    "FactoryAppException",
    "EmptyResponseError",
]


class FactoryAppException(Exception):
    """Basic Factory App exception."""


class UnexpectedError(Exception):
    """Internal Server Error."""

    def __init__(self):
        super().__init__("Unexpected Error")


class RequestError(Exception):
    """Request Error - basic class."""


class AuthorizationError(RequestError):
    """Unauthorized requests."""

    def __init__(self, msg: Optional[str] = None):
        super().__init__(
            f"The provided api key is invalid : {msg}."
            if msg
            else "Api key is missing."
        )


class MalformedRequest(RequestError):
    """Malformed Request Error."""

    def __init__(self, msg):
        super().__init__(msg)


class PayloadTooLarge(RequestError):
    """Payload too large Error."""

    def __init__(self, content_length: Union[float, int], max_content_length: int):
        super().__init__(
            f"The request is larger than the server is willing or able to process."
            f" Request length: {content_length}, but allowed is: {max_content_length}."
        )


class MethodNotAllowed(RequestError):
    """Method not allowed."""

    def __init__(self, method: str):
        super().__init__(f"Method: {method} not allowed.")


class ResourceLockedError(RequestError):
    """Resource is locked."""

    def __init__(self):
        super().__init__("The resource that is being accessed is locked.")


class EmptyResponseError(RequestError):
    """Response is empty."""

    def __init__(self, msg: str):
        super().__init__(msg)


class InternalError(RequestError):
    """Validation Error"""

    def __init__(self):
        super().__init__(
            "The request was well-formed but server could not properly decode transaction."
        )
