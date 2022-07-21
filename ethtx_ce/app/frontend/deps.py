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

import json
import logging
import re
import time
from secrets import compare_digest
from typing import Optional

import requests
from flask import request
from flask_httpauth import HTTPBasicAuth

from ..config import Config

log = logging.getLogger(__name__)

auth = HTTPBasicAuth()

eth_price: Optional[float] = None
eth_price_update: Optional[float] = None


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    """Verify user, return bool."""
    return username == Config.ETHTX_ADMIN_USERNAME and compare_digest(
        password, Config.ETHTX_ADMIN_PASSWORD
    )


def get_eth_price() -> Optional[float]:
    """
    Get current ETH price from coinbase.com
    Cache price for 60 seconds.
    """
    global eth_price, eth_price_update

    current_time = time.time()
    if (
        eth_price is None
        or eth_price_update is None
        or (current_time - eth_price_update) > 60
    ):
        response = requests.get(
            "https://api.coinbase.com/v2/prices/ETH-USD/buy", timeout=2
        )
        if response.status_code == 200:
            eth_price = float(json.loads(response.content)["data"]["amount"])
            eth_price_update = time.time()

    return eth_price


def extract_tx_hash_from_req() -> str:
    """Extract tx hash from request url."""
    hash_match = re.findall(r"(0x)?([A-Fa-f0-9]{64})", request.url)

    return (
        f"{hash_match[0][0]}{hash_match[0][1]}"
        if hash_match and len(hash_match[0]) == 2
        else ""
    )
