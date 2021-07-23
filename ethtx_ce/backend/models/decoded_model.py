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
from typing import List, Any, Optional

from . import JsonObject


class TransactionMetadata(JsonObject):
    chain_id: str
    block_number: int
    timestamp: datetime
    tx_hash: str
    sender: str
    receiver: str
    gas_used: int
    gas_price: int
    eth_price: float

    def __init__(
        self,
        chain_id: str,
        block_number: int,
        timestamp: datetime,
        tx_hash: str,
        sender: str,
        receiver: str,
        gas_used: int,
        gas_price: int,
        eth_price: float = None,
    ):
        self.chain_id = chain_id
        self.block_number = block_number
        self.timestamp = timestamp
        self.tx_hash = tx_hash
        self.sender = sender
        self.receiver = receiver
        self.gas_used = gas_used
        self.gas_price = gas_price
        self.eth_price = eth_price


class AddressInfo(JsonObject):
    address: str
    name: str
    badge: Optional[str]

    def __init__(self, address: str, name: str, badge: Optional[str] = ""):
        self.address = address
        self.name = name
        self.badge = badge


class Argument(JsonObject):
    name: str
    type: str
    value: Any

    def __init__(self, name: str, type: str, value: Any):
        self.name = name
        self.type = type
        self.value = value


class DecodedEvent(JsonObject):
    chain_id: str
    tx_hash: str
    contract: AddressInfo
    index: int
    event_signature: str
    event_name: str
    parameters: List[Argument]

    def __init__(
        self,
        chain_id: str,
        tx_hash: str,
        contract_address: str,
        contract_name: str,
        index: int,
        event_signature: str,
        event_name: str,
        parameters: List[Argument],
    ):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.contract = AddressInfo(contract_address, contract_name)
        self.contract_name = contract_name
        self.index = index
        self.event_signature = event_signature
        self.event_name = event_name
        self.parameters = parameters


class DecodedCall(JsonObject):
    chain_id: str
    tx_hash: str
    call_id: str
    call_type: str
    from_address: AddressInfo
    to_address: AddressInfo
    value: int
    function_signature: str
    function_name: str
    arguments: List[Argument]
    outputs: List[Argument]
    gas_used: int
    error: str
    status: bool
    sub_calls: List["DecodedCall"]

    def __init__(
        self,
        chain_id: str,
        tx_hash: str,
        call_id: str,
        call_type: str,
        from_address: str,
        from_name: str,
        to_address: str,
        to_name: str,
        value: int,
        function_signature: str,
        function_name: str,
        arguments: List[Argument],
        outputs: List[Argument],
        gas_used: int,
        error: str,
        status: bool,
        indent: int,
        sub_calls: Optional[List["DecodedCall"]] = None,
    ):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.call_id = call_id
        self.call_type = call_type
        self.from_address = AddressInfo(from_address, from_name)
        self.to_address = AddressInfo(to_address, to_name)
        self.to_name = to_name
        self.value = value
        self.function_signature = function_signature
        self.function_name = function_name
        self.arguments = arguments
        self.outputs = outputs
        self.gas_used = gas_used
        self.error = error
        self.status = status
        self.indent = indent
        self.sub_calls = sub_calls if sub_calls else []


class DecodedTransfer:
    from_address: AddressInfo
    to_address: AddressInfo
    token_address: Optional[str]
    token_symbol: str
    token_standard: Optional[str]
    value: float

    def __init__(
        self,
        from_address: AddressInfo,
        to_address: AddressInfo,
        token_standard: Optional[str],
        token_address: Optional[str],
        token_symbol: str,
        value: float,
    ):
        self.from_address = from_address
        self.to_address = to_address
        self.token_address = token_address
        self.token_symbol = token_symbol
        self.token_standard = token_standard
        self.value = value


class DecodedBalance:
    holder: AddressInfo
    tokens: List[dict]

    def __init__(self, holder: AddressInfo, tokens: List[dict]):
        self.holder = holder
        self.tokens = tokens


class FullDecodedTransaction(JsonObject):
    tx_metadata: TransactionMetadata
    events: List[DecodedEvent]
    calls: Optional[DecodedCall]
    transfers: List[DecodedTransfer]
    balances: List[DecodedBalance]
    status: bool

    def __init__(
        self,
        tx_metadata: TransactionMetadata,
        events: List[DecodedEvent],
        calls: Optional[DecodedCall],
        transfers: List[DecodedTransfer],
        balances: List[DecodedBalance],
    ):
        self.tx_metadata = tx_metadata
        self.events = events
        self.calls = calls
        self.transfers = transfers
        self.balances = balances
        self.status = False
