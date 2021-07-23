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

from __future__ import annotations

from typing import List

from hexbytes import HexBytes


class W3Block:
    def __init__(
        self,
        difficulty: int,
        extraData: HexBytes,
        gasLimit: int,
        gasUsed: int,
        hash: HexBytes,
        logsBloom: HexBytes,
        miner: str,
        nonce: HexBytes,
        number: int,
        parentHash: HexBytes,
        receiptsRoot: HexBytes,
        sha3Uncles: HexBytes,
        size: int,
        stateRoot: HexBytes,
        timestamp: int,
        totalDifficulty: int,
        transactions: List,
        transactionsRoot: HexBytes,
        uncles: List,
    ):
        self.difficulty = difficulty
        self.extraData = extraData
        self.gas_limit = gasLimit
        self.gas_used = gasUsed
        self.hash = hash
        self.logsBloom = logsBloom
        self.miner = miner
        self.nonce = nonce
        self.number = number
        self.parentHash = parentHash
        self.receiptsRoot = receiptsRoot
        self.sha3Uncles = sha3Uncles
        self.size = size
        self.stateRoot = stateRoot
        self.timestamp = timestamp
        self.totalDifficulty = totalDifficulty
        self.transactions = transactions
        self.transactionsRoot = transactionsRoot
        self.uncles = uncles


class W3Transaction:
    def __init__(
        self,
        blockHash: str,
        blockNumber: int,
        from_address: str,
        gas: int,
        gasPrice: int,
        hash: HexBytes,
        input: str,
        nonce: int,
        r: HexBytes,
        s: HexBytes,
        to: str,
        transactionIndex: int,
        v: int,
        value: int,
    ):
        self.blockHash = blockHash
        self.blockNumber = blockNumber
        self.from_address = from_address
        self.gas = gas
        self.gasPrice = gasPrice
        self.hash = hash
        self.input = input
        self.nonce = nonce
        self.r = r
        self.s = s
        self.to_address = to
        self.transactionIndex = transactionIndex
        self.v = v
        self.value = value


class W3Receipt:
    def __init__(
        self,
        blockHash: HexBytes,
        blockNumber: int,
        contractAddress: str,
        cumulativeGasUsed: int,
        from_address: str,
        gasUsed: int,
        logs: List,
        logsBloom: HexBytes,
        root: str,
        status: int,
        to_address: str,
        transactionHash: HexBytes,
        transactionIndex: int,
    ):
        self.root = root
        self.blockHash = blockHash
        self.blockNumber = blockNumber
        self.contractAddress = contractAddress
        self.cumulativeGasUsed = cumulativeGasUsed
        self.from_address = from_address
        self.gasUsed = gasUsed
        self.logs = [
            W3Log(
                log.address,
                log.blockHash,
                log.blockNumber,
                log.data,
                log.logIndex,
                log.removed,
                log.topics,
                log.transactionHash,
                log.transactionIndex,
            )
            for log in logs
        ]
        self.logsBloom = logsBloom
        self.status = status
        self.to_address = to_address
        self.transactionHash = transactionHash
        self.transactionIndex = transactionIndex


class W3Log:
    address: str
    blockHash: HexBytes
    blockNumber: int
    data: str
    logIndex: int
    removed: bool
    topics: List[HexBytes]
    transactionHash: HexBytes
    transactionIndex: int

    def __init__(
        self,
        address: str,
        blockHash: HexBytes,
        blockNumber: int,
        data: str,
        logIndex: int,
        removed: bool,
        topics: List[HexBytes],
        transactionHash: HexBytes,
        transactionIndex: int,
    ):
        self.address = address
        self.blockHash = blockHash
        self.blockNumber = blockNumber
        self.data = data
        self.logIndex = logIndex
        self.removed = removed
        self.topics = topics
        self.transactionHash = transactionHash
        self.transactionIndex = transactionIndex


class W3CallTree:
    type: str
    from_address: str
    to_address: str
    input: str
    output: str
    calls: List[W3CallTree]
    value: str
    time: str
    gas: str
    gasUsed: str
    error: str

    def __init__(
        self,
        type: str,
        from_address: str,
        to_address: str,
        input: str,
        output: str,
        value: str = None,
        time: str = None,
        gas: str = None,
        gasUsed: str = None,
        error: str = None,
    ):
        self.calls = []
        self.type = type
        self.from_address = from_address
        self.to_address = to_address
        self.input = input
        self.output = output
        self.value = value
        self.time = time
        self.gas = gas
        self.gasUsed = gasUsed
        self.error = error
