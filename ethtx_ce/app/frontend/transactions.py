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

from ethtx.models.decoded_model import DecodedTransaction
from flask import Blueprint, render_template, current_app

from . import frontend_route, deps

log = logging.getLogger(__name__)

bp = Blueprint("transactions", __name__)


@frontend_route(bp, "/<string:tx_hash>/")
@frontend_route(bp, "/<string:chain_id>/<string:tx_hash>/")
def read_decoded_transaction(
    tx_hash: str, chain_id: Optional[str] = None
) -> "show_transaction_page":
    tx_hash = tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash

    chain_id = chain_id or current_app.ethtx.default_chain
    decoded_transaction = current_app.ethtx.decoders.decode_transaction(
        chain_id=chain_id, tx_hash=tx_hash
    )
    decoded_transaction.metadata.timestamp = (
        decoded_transaction.metadata.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    )

    return show_transaction_page(decoded_transaction)


def show_transaction_page(data: DecodedTransaction) -> render_template:
    """Render transaction/exception page."""
    return (
        render_template(
            "transaction.html",
            eth_price=deps.get_eth_price(),
            transaction=data.metadata,
            events=data.events,
            call=data.calls,
            transfers=data.transfers,
            balances=data.balances,
        ),
        200,
    )
