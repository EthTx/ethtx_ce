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

from flask import Blueprint

from ethtx_ce.backend.api import route
from ethtx_ce.backend.api.core.decorators import response
from ethtx_ce.backend.api.service import DecoderService

log = logging.getLogger(__name__)
transactions_bp = Blueprint("transactions", __name__)


@route(transactions_bp, "/transactions/<string:chain_id>/<string:tx_hash>")
@response(200)
def read_decoded_transaction(chain_id: str, tx_hash: str):
    """ Decode transaction. """
    tx_hash = tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash
    decoded = DecoderService.decode_transaction(chain_id=chain_id, tx_hash=tx_hash)

    return decoded
