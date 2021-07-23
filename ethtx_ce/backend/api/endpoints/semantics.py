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

from flask import Blueprint

from ethtx_ce.backend.api import route
from ethtx_ce.backend.api.core.decorators import response
from ethtx_ce.backend.api.service import DecoderService

semantics_bp = Blueprint("semantics", __name__)


@route(semantics_bp, "/semantics/<string:chain_id>/<string:address>")
@response(200)
def read_raw_semantic(chain_id: str, address: str):
    """ Get raw semantic. """
    return DecoderService.decode_semantic(chain_id=chain_id, address=address)
