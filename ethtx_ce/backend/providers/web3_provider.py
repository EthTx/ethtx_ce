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
import os
from functools import lru_cache
from typing import List, Dict

from web3 import Web3
from web3.datastructures import AttributeDict

from ethtx_ce.config import EthConfig
from ethtx_ce.backend.exceptions import Web3ConnectionException, ProcessingException
from ethtx_ce.backend.models.w3_model import (
    W3Block,
    W3Transaction,
    W3Receipt,
    W3CallTree,
)
from ethtx_ce.semantics.standards import erc20
from ethtx_ce.backend.validators import (
    assert_chain_id_is_correct,
    assert_tx_hash_is_correct,
)
from ethtx_ce.helpers import Singleton, ExecutionTimer

log = logging.getLogger(__name__)


def connect_chain(
    http_hook: str = None, ipc_hook: str = None, ws_hook: str = None
) -> Web3 or None:
    if http_hook:
        method = "HTTP"
        provider = Web3.HTTPProvider
        hook = http_hook
    elif ipc_hook:
        method = "IPC"
        provider = Web3.IPCProvider
        hook = ipc_hook
    elif ws_hook:
        method = "Websocket"
        provider = Web3.WebsocketProvider
        hook = ws_hook
    else:
        method = "IPC"
        provider = Web3.IPCProvider
        hook = "\\\\.\\pipe\\geth.ipc"

    try:
        w3 = Web3(provider(hook, request_kwargs={"timeout": 600}))
        if w3.isConnected():
            log.info(
                "Connected to %s: %s with latest block %s.",
                method,
                hook,
                w3.eth.block_number,
            )
            return w3
        else:
            log.info("%s connection to %s failed.", method, hook)
            raise Web3ConnectionException()
    except Exception as exc:
        log.warning("Node connection %s: %s failed.", method, hook, exc_info=exc)
        raise


class Web3Provider(metaclass=Singleton):
    chain: Web3

    def __init__(self, chain_id: str = EthConfig.DEFAULT_CHAIN):
        assert_chain_id_is_correct(chain_id)
        self.chain = connect_chain(http_hook=EthConfig.NODES_WITH_URLS[chain_id])

    # get the raw block data from the node
    @lru_cache(maxsize=128)
    def get_block(self, block_number: int) -> W3Block:

        with ExecutionTimer(f"web3_get_block_{block_number}"):
            raw_block = self.chain.eth.get_block(block_number)
            block = W3Block(
                raw_block.difficulty,
                raw_block.extraData,
                raw_block.gasLimit,
                raw_block.gasUsed,
                raw_block.hash,
                raw_block.logsBloom,
                raw_block.miner,
                raw_block.get("nonce", 0),
                raw_block.number,
                raw_block.parentHash,
                raw_block.receiptsRoot,
                raw_block.sha3Uncles,
                raw_block.size,
                raw_block.stateRoot,
                raw_block.timestamp,
                raw_block.totalDifficulty,
                raw_block.transactions,
                raw_block.transactionsRoot,
                raw_block.uncles,
            )

        return block

    # get the raw transaction data from the node
    @lru_cache(maxsize=128)
    def get_transaction(self, tx_hash: str) -> W3Transaction:
        with ExecutionTimer(f"web3_get_tx_{tx_hash}"):
            raw_tx = self.chain.eth.get_transaction(tx_hash)
            transaction = W3Transaction(
                raw_tx.blockHash,
                raw_tx.blockNumber,
                raw_tx["from"],
                raw_tx.gas,
                raw_tx.gasPrice,
                raw_tx.hash,
                raw_tx.input,
                raw_tx.nonce,
                raw_tx.r,
                raw_tx.s,
                raw_tx.to,
                raw_tx.transactionIndex,
                raw_tx.v,
                raw_tx.value,
            )

        return transaction

    # get the raw transaction receipt data from the node
    @lru_cache(maxsize=128)
    def get_transaction_receipt(self, tx_hash: str) -> W3Receipt:
        with ExecutionTimer(f"web3_get_tx_{tx_hash}"):
            raw_receipt = self.chain.eth.getTransactionReceipt(tx_hash)
            _root = raw_receipt.root if hasattr(raw_receipt, "root") else None
            receipt = W3Receipt(
                raw_receipt.blockHash,
                raw_receipt.blockNumber,
                raw_receipt.contractAddress,
                raw_receipt.cumulativeGasUsed,
                raw_receipt["from"],
                raw_receipt.gasUsed,
                raw_receipt.logs,
                raw_receipt.logsBloom,
                _root,
                raw_receipt.status,
                raw_receipt.to,
                raw_receipt.transactionHash,
                raw_receipt.transactionIndex,
            )

        return receipt

    @lru_cache(maxsize=128)
    def get_calls(self, tx_hash: str) -> W3CallTree:
        assert_tx_hash_is_correct(tx_hash)
        with ExecutionTimer(f"web3_get_calls_{tx_hash}"):
            # tracer is a temporary fixed implementation of geth tracer
            tracer = open(
                os.path.join(os.path.dirname(__file__), "static/tracer.js")
            ).read()
            response = self.chain.manager.request_blocking(
                "debug_traceTransaction", [tx_hash, {"tracer": tracer}]
            )

        return self._create_call_from_debug_trace_tx(response)

    # get the contract bytecode hash from the node
    @lru_cache(maxsize=128)
    def get_code_hash(self, contract_address: str) -> str:
        with ExecutionTimer(f"web3_get_code_hash_{contract_address}"):
            byte_code = self.chain.eth.get_code(
                Web3.toChecksumAddress(contract_address)
            )
            code_hash = Web3.keccak(byte_code).hex()
        return code_hash

    # get the erc20 token data from the node
    def get_erc20_token(self, token_address, contract_name, functions):

        name_abi = symbol_abi = decimals_abi = ""

        if functions:
            for function in functions.values():
                if (
                    function.name == "name"
                    and len(function.inputs) == 0
                    and len(function.outputs) == 1
                ):
                    name_type = function.outputs[0].parameter_type
                    name_abi = (
                        '{"name":"name", "constant":true, "payable":false, "type":"function", '
                        ' "inputs":[], "outputs":[{"name":"","type":"%s"}]}' % name_type
                    )

                elif (
                    function.name == "symbol"
                    and len(function.inputs) == 0
                    and len(function.outputs) == 1
                ):
                    symbol_type = function.outputs[0].parameter_type
                    symbol_abi = (
                        '{"name":"symbol", "constant":true, "payable":false,"type":"function", '
                        ' "inputs":[], "outputs":[{"name":"","type":"%s"}]}'
                        % symbol_type
                    )

                elif (
                    function.name in ["decimals", "dec"]
                    and len(function.inputs) == 0
                    and len(function.outputs) == 1
                ):
                    decimals_type = function.outputs[0].parameter_type
                    decimals_abi = (
                        '{"name":"decimals", "constant":true, "payable":false,"type":"function", '
                        ' "inputs":[], "outputs":[{"name":"","type":"%s"}]}'
                        % decimals_type
                    )

        abi = f'[{",".join([name_abi, symbol_abi, decimals_abi])}]'

        try:
            with ExecutionTimer(f"web3_get_erc20_{token_address}"):
                token = self.chain.eth.contract(
                    address=Web3.toChecksumAddress(token_address), abi=abi
                )
                name = token.functions.name().call() if name_abi else contract_name
                symbol = (
                    token.functions.symbol().call() if symbol_abi else contract_name
                )
                decimals = token.functions.decimals().call() if decimals_abi else 18
        except:
            name = symbol = contract_name
            decimals = 18

        return dict(address=token_address, symbol=symbol, name=name, decimals=decimals)

    # guess if the contract is and erc20 token and get the data
    def guess_erc20_token(self, contract_address):

        with ExecutionTimer(
            f"web3_get_code_{Web3.toChecksumAddress(contract_address)}"
        ):
            byte_code = self.chain.eth.get_code(
                Web3.toChecksumAddress(contract_address)
            ).hex()

        if all(
            "63" + signature[2:] in byte_code
            for signature in (
                erc20.erc20_transfer_function.signature,
                erc20.erc20_transferFrom_function.signature,
                erc20.erc20_approve_function.signature,
            )
        ) and all(
            signature[2:] in byte_code
            for signature in (
                erc20.erc20_transfer_event.signature,
                erc20.erc20_approval_event.signature,
            )
        ):

            name_abi = (
                '{"name":"name", "constant":true, "payable":false,'
                ' "type":"function", "inputs":[], "outputs":[{"name":"","type":"string"}]}'
            )
            symbol_abi = (
                '{"name":"symbol", "constant":true, "payable":false,'
                '"type":"function", "inputs":[], "outputs":[{"name":"","type":"string"}]}'
            )
            decimals_abi = (
                '{"name":"decimals", "constant":true, "payable":false,'
                '"type":"function",  "inputs":[], "outputs":[{"name":"","type":"uint8"}]}'
            )

            abi = f'[{",".join([name_abi, symbol_abi, decimals_abi])}]'

            try:
                with ExecutionTimer(
                    f"web3_get_contract_{Web3.toChecksumAddress(contract_address)}"
                ):
                    token = self.chain.eth.contract(
                        address=Web3.toChecksumAddress(contract_address), abi=abi
                    )
                name = token.functions.name().call()
                symbol = token.functions.symbol().call()
                decimals = token.functions.decimals().call()

                return dict(
                    address=contract_address,
                    symbol=symbol,
                    name=name,
                    decimals=decimals,
                )

            except Exception:
                raise ProcessingException("during erx20 token guess")

        return None

    @staticmethod
    def _create_call_from_debug_trace_tx(input_rpc: AttributeDict) -> W3CallTree:
        def prep_raw_dict(dct: [AttributeDict, Dict]):
            if not isinstance(dct, dict):
                dct = dct.__dict__
            dct["from_address"] = dct.pop("from")
            dct["to_address"] = dct.pop("to")
            dct["input"] = dct.pop("input", "0x")
            dct["output"] = dct.pop("output", "0x")
            child_calls = dct.pop("calls", [])
            return dct, child_calls

        obj = input_rpc.__dict__
        tmp_call_tree = []

        w3input, main_parent_calls = prep_raw_dict(obj)
        main_parent = W3CallTree(**w3input)
        for main_parent_call in main_parent_calls:
            w3input, main_parent_calls = prep_raw_dict(main_parent_call)
            main_parent_child = W3CallTree(**w3input)
            main_parent.calls.append(main_parent_child)
            if len(main_parent_calls) > 0:
                tmp_call_tree.append(
                    {"parent": main_parent_child, "children": main_parent_calls}
                )

        while len(tmp_call_tree) != 0:
            new_call_tree = []

            for pair in tmp_call_tree:

                parent_call: W3CallTree = pair["parent"]
                child_calls: List = pair["children"]

                if child_calls is not None:
                    for child_call in child_calls:
                        w3input, child_child_call = prep_raw_dict(child_call)
                        child = W3CallTree(**w3input)
                        parent_call.calls.append(child)

                        if len(child_call) > 0:
                            new_call_tree.append(
                                {"parent": child, "children": child_child_call}
                            )

            tmp_call_tree = new_call_tree

        return main_parent
