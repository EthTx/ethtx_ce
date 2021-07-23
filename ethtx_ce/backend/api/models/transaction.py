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

from datetime import datetime
from typing import Optional


class PayloadTransaction:
    """ POST Payload Transaction Metadata. """

    chain_id: str
    tx_hash: str
    block_number: int
    sender: str
    receiver: str

    timestamp: datetime
    gas_price: int
    tx_index: int
    tx_value: int
    gas_used: int
    status: bool

    def __init__(
        self,
        tx_hash: str,
        block_number: int,
        sender: str,
        gas_price: int,
        transaction_index: int,
        value: int,
        gas_used: int,
        status: bool,
        timestamp,
        chain_id: str,
        receiver: Optional[str] = None,
    ):
        self.tx_hash = tx_hash
        self.chain_id = chain_id
        self.sender = sender
        self.receiver = receiver

        self.block_number = block_number
        self.gas_price = gas_price
        self.from_address = sender.lower()
        self.to_address = receiver.lower() if receiver else None
        self.tx_index = transaction_index
        self.tx_value = value

        self.gas_used = gas_used
        self.status = status

        self.timestamp = datetime.fromtimestamp(timestamp)
