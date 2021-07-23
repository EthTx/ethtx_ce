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

from functools import lru_cache
from typing import Optional

from ethtx_ce.backend.models.semantics_model import (
    AddressSemantics,
    ContractSemantics,
    ParameterSemantics,
    ERC20Semantics,
)
from ethtx_ce.backend.processors.decoders.semantics import decode_events_and_functions
from ethtx_ce.backend.providers.etherscan_provider import EtherscanProvider
from ethtx_ce.backend.providers.semantic_providers.semantics_database import (
    SemanticsDatabase,
)
from ethtx_ce.backend.providers.web3_provider import Web3Provider
from ethtx_ce.semantics.protocols_router import amend_contract_semantics
from ethtx_ce.semantics.standards.erc20 import ERC20_FUNCTIONS, ERC20_EVENTS
from ethtx_ce.semantics.standards.erc721 import ERC721_FUNCTIONS, ERC721_EVENTS


class SemanticsRepository:
    """ Semantics Repository. """

    def __init__(
        self,
        database_connection: SemanticsDatabase,
        etherscanProvider: EtherscanProvider = None,
    ):
        self.database = database_connection
        self.etherscan = etherscanProvider or EtherscanProvider()

    @lru_cache(maxsize=128)
    def _get_semantics(self, chain_id: str, address: str) -> Optional[AddressSemantics]:

        ZERO_HASH = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"

        address_semantics = self.database.get_raw_semantics(chain_id, address)
        if not address_semantics:
            # try to read the semantics form the Etherscan provider
            provider = Web3Provider(chain_id)
            code_hash = provider.get_code_hash(address)

            if code_hash != ZERO_HASH:
                # smart contract
                raw_semantics, decoded = self.etherscan.get_contract_abi(
                    chain_id, address
                )
                if decoded and raw_semantics:
                    # raw semantics received from Etherscan
                    events, functions = decode_events_and_functions(
                        raw_semantics["abi"]
                    )
                    standard, standard_semantics = self._decode_standard_semantics(
                        chain_id, address, raw_semantics["name"], events, functions
                    )
                    erc20_semantics = (
                        standard_semantics if standard == "ERC20" else None
                    )
                    contract_semantics = ContractSemantics(
                        code_hash, raw_semantics["name"], events, functions, dict()
                    )
                    address_semantics = AddressSemantics(
                        chain_id,
                        address,
                        raw_semantics["name"],
                        True,
                        contract_semantics,
                        standard,
                        erc20_semantics,
                    )

                else:
                    # try to guess if the address is a toke
                    potential_erc20_semantics = provider.guess_erc20_token(address)
                    if potential_erc20_semantics:
                        standard = "ERC20"
                        erc20_semantics = ERC20Semantics(
                            potential_erc20_semantics["name"],
                            potential_erc20_semantics["symbol"],
                            potential_erc20_semantics["decimals"],
                        )
                    else:
                        standard = None
                        erc20_semantics = None

                    contract_semantics = ContractSemantics(
                        code_hash, address, dict(), dict(), dict()
                    )
                    address_semantics = AddressSemantics(
                        chain_id,
                        address,
                        address,
                        True,
                        contract_semantics,
                        standard,
                        erc20_semantics,
                    )

            else:
                # externally owned address
                contract_semantics = ContractSemantics(
                    ZERO_HASH, "EOA", dict(), dict(), dict()
                )
                address_semantics = AddressSemantics(
                    chain_id, address, address, False, contract_semantics, None, None
                )

            self.update_semantics(address_semantics)

        # amend semantics with locally stored updates
        amend_contract_semantics(address_semantics.contract)

        return address_semantics

    @staticmethod
    def _decode_standard_semantics(chain_id, address, name, events, functions):

        standard = None
        standard_semantics = None

        if all(erc20_event in events for erc20_event in ERC20_EVENTS) and all(
            erc20_function in functions for erc20_function in ERC20_FUNCTIONS
        ):
            standard = "ERC20"
            try:
                provider = Web3Provider(chain_id)
                token_data = provider.get_erc20_token(address, name, functions)
                standard_semantics = ERC20Semantics(
                    token_data["name"], token_data["symbol"], token_data["decimals"]
                )
            except:
                standard_semantics = ERC20Semantics(name, name, 18)
        elif all(erc721_event in events for erc721_event in ERC721_EVENTS) and all(
            erc721_function in functions for erc721_function in ERC721_FUNCTIONS
        ):
            standard = "ERC721"
            standard_semantics = None

        return standard, standard_semantics

    @lru_cache(maxsize=128)
    def get_event_abi(self, chain_id, address, signature):

        semantics = self._get_semantics(chain_id, address)
        event_semantics = (
            semantics.contract.events.get(signature) if semantics else None
        )

        return event_semantics

    @lru_cache(maxsize=128)
    def get_transformations(self, chain_id, address, signature):

        semantics = self._get_semantics(chain_id, address)
        if semantics:
            transformations = semantics.contract.transformations.get(signature)
        else:
            transformations = None

        return transformations

    @lru_cache(maxsize=128)
    def get_anonymous_event_abi(self, chain_id, address):

        semantics = self._get_semantics(chain_id, address)
        event_semantics = None
        if semantics:
            anonymous_events = {
                signature
                for signature, event in semantics.contract.events.items()
                if event.anonymous
            }
            if len(anonymous_events) == 1:
                event_signature = anonymous_events.pop()
                event_semantics = semantics.contract.events[event_signature]

        return event_semantics

    @lru_cache(maxsize=128)
    def get_function_abi(self, chain_id, address, signature):

        semantics = self._get_semantics(chain_id, address)
        function_semantics = (
            semantics.contract.functions.get(signature) if semantics else None
        )

        return function_semantics

    @lru_cache(maxsize=128)
    def get_constructor_abi(self, chain_id, address):

        semantics = self._get_semantics(chain_id, address)
        constructor_semantics = (
            semantics.contract.functions.get("constructor") if semantics else None
        )
        if constructor_semantics:
            constructor_semantics.outputs.append(
                ParameterSemantics("__create_output__", "ignore", [], False, True)
            )

        return constructor_semantics

    def get_address_label(self, chain_id, address, token_proxies=None):

        semantics = self._get_semantics(chain_id, address)
        if semantics.erc20:
            contract_label = semantics.erc20.symbol
        elif token_proxies and address in token_proxies:
            contract_label = token_proxies[address][1] + "_proxy"
        else:
            contract_label = semantics.name if semantics and semantics.name else address

        return contract_label

    @lru_cache(maxsize=128)
    def check_is_contract(self, chain_id, address):

        semantics = self._get_semantics(chain_id, address)
        is_contract = semantics is not None and semantics.is_contract

        return is_contract

    @lru_cache(maxsize=128)
    def get_standard(self, chain_id, address):

        semantics = self._get_semantics(chain_id, address)
        standard = semantics.standard if semantics is not None else None

        return standard

    def get_token_data(self, chain_id, address, token_proxies=None):

        semantics = self._get_semantics(chain_id, address)
        if semantics and semantics.erc20:
            token_name = (
                semantics.erc20.name if semantics and semantics.erc20 else address
            )
            token_symbol = (
                semantics.erc20.symbol if semantics and semantics.erc20 else "Unknown"
            )
            token_decimals = (
                semantics.erc20.decimals if semantics and semantics.erc20 else 18
            )
        elif token_proxies and address in token_proxies:
            token_name, token_symbol, token_decimals = token_proxies[address]
        else:
            token_name = address
            token_symbol = "Unknown"
            token_decimals = 18

        return token_name, token_symbol, token_decimals

    def update_address(self, chain_id, address, contract):

        updated_address = {"network": chain_id, "address": address, **contract}
        self.database.insert_address(address=updated_address, update_if_exist=True)

        return updated_address

    def update_semantics(self, semantics):

        if not semantics:
            return

        address_semantics = semantics.json(False)
        contract_semantics = semantics.contract.json()

        self.database.insert_contract(contract_semantics, update_if_exist=True)
        self.database.insert_address(address_semantics, update_if_exist=True)
