# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

import logging
import os
from typing import Optional

from ethtx.models.decoded_model import DecodedTransaction
from flask import Blueprint, render_template, current_app, request

from . import frontend_route, deps

log = logging.getLogger(__name__)

bp = Blueprint("transactions", __name__)


@frontend_route(bp, "/<string:tx_hash>/")
@frontend_route(bp, "/<string:chain_id>/<string:tx_hash>/")
def read_decoded_transaction(
    tx_hash: str, chain_id: Optional[str] = None
) -> "show_transaction_page":
    tx_hash = tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash

    refresh_semantics = "refresh" in request.args

    if refresh_semantics:
        refresh_secure_key = request.args["refresh"]
        if refresh_secure_key != os.environ["SEMANTIC_REFRESH_KEY"]:
            return "Invalid semantics refresh key"

        log.info(f"Decoding tx {tx_hash} with semantics refresh")

    chain_id = chain_id or current_app.ethtx.default_chain
    decoded_transaction = current_app.ethtx.decoders.decode_transaction(
        chain_id=chain_id, tx_hash=tx_hash, recreate_semantics=refresh_semantics
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
