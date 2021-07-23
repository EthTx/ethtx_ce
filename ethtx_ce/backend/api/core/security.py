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

from typing import NoReturn

from flask import request

from ethtx_ce.backend.exceptions import ResourceLockedError

# security_bp = Blueprint("api_sec", __name__)

WHITE_LIST = ["127.0.0.1", "0.0.0.0"]


# @security_bp.before_app_request
def block_external_traffic() -> NoReturn:
    """ Block external traffic. Same instance only allowed. """
    ip = request.environ.get("REMOTE_ADDR")
    if not any((ip not in WHITE_LIST, ip != request.host.split(":")[0])):
        raise ResourceLockedError()
