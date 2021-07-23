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

import re

from ethtx_ce.config import EthConfig
from .exceptions import InvalidTransactionHash


def assert_tx_hash_is_correct(tx_hash) -> None:
    """ Check if tx_hash is correct """
    tx_hash_regex = "^0x([A-Fa-f0-9]{64})$"
    if not re.match(tx_hash_regex, tx_hash):
        raise InvalidTransactionHash(tx_hash)


def assert_chain_id_is_correct(chain_id: str) -> None:
    """ Check if chain_id is correct """
    assert chain_id in EthConfig.NODES_WITH_URLS.keys()
