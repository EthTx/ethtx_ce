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
from typing import Optional

from flask import Blueprint, current_app

from .. import api_route
from ..decorators import response

log = logging.getLogger(__name__)
transactions_bp = Blueprint("api_transactions", __name__)


@api_route(transactions_bp, "/transactions/<string:tx_hash>")
@api_route(transactions_bp, "/transactions/<string:chain_id>/<string:tx_hash>")
@response(200)
def read_decoded_transaction(tx_hash: str, chain_id: Optional[str] = None):
    """Decode transaction."""
    tx_hash = tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash

    chain_id = chain_id or current_app.ethtx.default_chain
    decoded_transaction = current_app.ethtx.decoders.decode_transaction(
        chain_id=chain_id, tx_hash=tx_hash
    )
    decoded_transaction.metadata.timestamp = (
        decoded_transaction.metadata.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    )
    return decoded_transaction.dict()
