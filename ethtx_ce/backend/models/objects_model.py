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
from typing import Dict, List, Optional

from ethtx_ce.config import EthConfig

from .w3_model import W3CallTree, W3Log
from ..providers.web3_provider import Web3Provider
from ..validators import assert_tx_hash_is_correct


class Block:
    chain_id: str
    block_number: int
    block_hash: str
    timestamp: datetime
    parent_hash: str
    miner: str
    gas_limit: int
    gas_used: int
    tx_count: int

    def __init__(
        self,
        block_number,
        chain_id: str = EthConfig.DEFAULT_CHAIN,
        web3provider: Web3Provider = None,
    ):
        if web3provider is None:
            web3provider = Web3Provider()
        self.block_number = block_number
        self.chain_id = chain_id

        self._create_from_w3(web3provider)

    def _create_from_w3(self, provider) -> None:
        w3block = provider.get_block(self.block_number)

        self.block_hash = w3block.hash.hex()
        self.timestamp = datetime.fromtimestamp(w3block.timestamp)
        self.parent_hash = w3block.parentHash.hex()
        self.miner = w3block.miner.lower()
        self.gas_limit = w3block.gas_limit
        self.gas_used = w3block.gas_used
        self.tx_count = len(w3block.transactions)


class Transaction:
    chain_id: str
    tx_hash: str
    block_number: int
    timestamp: datetime
    gas_price: int
    from_address: str
    to_address: str
    tx_index: int
    tx_value: int
    gas_limit: int
    gas_used: int
    created_address: str
    success: bool

    gas_refund: int
    return_value: str
    exception_error: str
    exception_error_type: str
    revert_reason: str

    def __init__(
        self,
        tx_hash: str,
        chain_id: str = EthConfig.DEFAULT_CHAIN,
        web3provider: Web3Provider = None,
    ):
        assert_tx_hash_is_correct(tx_hash)

        self.tx_hash = tx_hash
        self.chain_id = chain_id
        self._create_from_w3(web3provider)

    def _create_from_w3(self, provider: Web3Provider) -> None:
        if provider is None:
            provider = Web3Provider(self.chain_id)

        w3transaction = provider.get_transaction(self.tx_hash)
        w3receipt = provider.get_transaction_receipt(self.tx_hash)
        w3block = provider.get_block(w3transaction.blockNumber)

        self.block_number = w3transaction.blockNumber
        self.gas_price = w3transaction.gasPrice
        self.from_address = w3transaction.from_address.lower()
        self.to_address = (
            w3transaction.to_address.lower() if w3transaction.to_address else None
        )
        self.tx_index = w3transaction.transactionIndex
        self.tx_value = w3transaction.value
        self.gas_limit = w3transaction.gas

        self.gas_used = w3receipt.gasUsed
        self.created_address = w3receipt.contractAddress
        self.status = w3receipt.status

        self.timestamp = datetime.fromtimestamp(w3block.timestamp)


class Event:
    chain_id: str
    timestamp: datetime
    tx_hash: str
    contract: str
    topic: List[str]
    log_data: Optional[str]
    log_index: int

    def __init__(self, chain_id: str, tx_hash: str, timestamp: datetime, log: W3Log):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.timestamp = timestamp
        self._create_from_log(log)

    def _create_from_log(self, log: W3Log) -> None:
        self.contract = log.address.lower()
        self.log_index = log.logIndex
        self.log_data = log.data

        self.topics = []
        for i in range(len(log.topics)):
            self.topics.append(log.topics[i].hex())


class Call:
    chain_id: str
    block_number: int
    timestamp: str
    tx_hash: str
    call_id: int
    call_type: str
    call_gas: int
    from_address: str
    call_value: int
    call_data: str
    return_value: str
    gas_used: int
    gas_refund: int
    exception_error: str
    exception_error_type: str
    revert_reason: str
    success: bool
    status: bool
    subcalls: list

    def __init__(
        self,
        tx_hash: str = None,
        chain_id: str = EthConfig.DEFAULT_CHAIN,
        w3_call_tree: W3CallTree = None,
    ):

        self.chain_id = chain_id
        self.subcalls = []

        if tx_hash is not None:
            tree = Web3Provider(chain_id).get_calls(tx_hash)
            self._create_from_w3_call_tree(tree)

        if w3_call_tree is not None:
            self._hydrate_from_w3_call_tree(w3_call_tree)

        self.tx_hash = tx_hash

    def _hydrate_from_w3_call_tree(self, w3_call_tree: W3CallTree) -> None:

        self.from_address = w3_call_tree.from_address
        self.to_address = w3_call_tree.to_address
        self.call_value = int(w3_call_tree.value, 16) if w3_call_tree.value else 0
        self.call_type = w3_call_tree.type.lower()
        self.call_data = w3_call_tree.input
        self.return_value = w3_call_tree.output
        self.timestamp = w3_call_tree.time
        self.gas_used = int(w3_call_tree.gasUsed, 16) if w3_call_tree.gasUsed else None
        self.call_gas = int(w3_call_tree.gas, 16) if w3_call_tree.gas else None
        self.error = w3_call_tree.error
        self.status = self.error is None

    def _create_from_w3_call_tree(self, w3_call_tree: W3CallTree) -> None:

        self._hydrate_from_w3_call_tree(w3_call_tree)
        level: Dict[Call, List[W3CallTree]] = {self: w3_call_tree.calls}

        while len(level) != 0:
            new_level = {}
            for parent, children in level.items():

                for child in children:
                    call_child = Call(w3_call_tree=child, chain_id=self.chain_id)
                    parent.subcalls.append(call_child)
                    new_level[call_child] = child.calls

            level = new_level


class FullTransaction:
    chain_id: str
    tx_hash: str

    transaction: Transaction
    block: Block = None
    events: List[Event] = []
    root_call: Optional[Call] = None

    def __init__(self, tx_hash: str, chain_id: Optional[str] = EthConfig.DEFAULT_CHAIN):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.transaction = Transaction(tx_hash, chain_id)
        self.block = Block(self.transaction.block_number, chain_id)
        self.events = self._get_events()
        try:
            self.root_call = Call(self.tx_hash, chain_id)
        except:
            self.root_call = None

    def _get_events(self) -> List[Event]:
        provider = Web3Provider(self.chain_id)
        receipt = provider.get_transaction_receipt(self.tx_hash)
        events = []
        for log in receipt.logs:
            events.append(Event(self.chain_id, self.tx_hash, self.block.timestamp, log))

        return events
