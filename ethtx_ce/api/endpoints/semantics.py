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
from typing import Optional

from flask import Blueprint, current_app

from .. import api_route
from ..decorators import response

semantics_bp = Blueprint("api_semantics", __name__)


@api_route(semantics_bp, "/semantics/<string:address>")
@api_route(semantics_bp, "/semantics/<string:chain_id>/<string:address>")
@response(200)
def read_raw_semantic(address: str, chain_id: Optional[str] = None):
    """Get raw semantic."""
    raw_semantics = current_app.ethtx.semantics.get_raw_semantics(
        chain_id=chain_id, address=address
    )
    return raw_semantics.dict()
