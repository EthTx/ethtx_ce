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

from abc import ABC, abstractmethod
from typing import Optional, Any, List, Dict

from ...models.decoded_model import TransactionMetadata, DecodedCall, DecodedTransfer
from ...models.objects_model import Call, FullTransaction, Event
from ...providers.semantic_providers.semantics_repository import SemanticsRepository


class ABIBasic:
    """ ABI Basic class """

    def __init__(self, repository: SemanticsRepository):
        self.repository = repository

    @staticmethod
    def get_delegations(call: Call) -> Dict[str, set]:
        """ Get delegations. """
        delegations = {}

        if not call:
            return delegations

        calls_queue = [call]
        while calls_queue:

            call = calls_queue.pop()
            for _, sub_call in enumerate(call.subcalls):
                calls_queue.insert(0, sub_call)

            if call.call_type == "delegatecall":
                if call.from_address not in delegations:
                    delegations[call.from_address] = set()
                delegations[call.from_address].add(call.to_address)

        return delegations

    def get_token_proxies(
        self, delegations: Dict[str, set], tx_metadata: TransactionMetadata
    ) -> Dict[str, Dict]:
        """ Get token proxies """
        token_proxies = {}

        for delegator in delegations:
            delegator_semantic = self.repository.get_token_data(
                tx_metadata.chain_id, delegator
            )
            if (
                delegator_semantic[0] == delegator
                and delegator_semantic[1] == "Unknown"
            ):
                for delegate in delegations[delegator]:
                    delegate_semantic = self.repository.get_token_data(
                        tx_metadata.chain_id, delegate
                    )
                    if (
                        delegate_semantic[0] != delegate
                        and delegate_semantic[1] != "Unknown"
                    ):
                        token_proxies[delegator] = delegate_semantic
                        break

        return token_proxies


class ABISubmoduleAbc(ABC, ABIBasic):
    """ Abi submodule properties. """

    @abstractmethod
    def decode(self, *args, **kwargs) -> Any:
        """ Return decoded object. """
        ...


class ABIProcessorAbc(ABC, ABIBasic):
    def __init__(self, repository: SemanticsRepository, strict: Optional[bool] = False):
        super().__init__(repository)
        self.strict = strict

    @abstractmethod
    def decode_with_abi(self, transaction: FullTransaction):
        """ Decode full transaction. """
        ...

    @abstractmethod
    def decode_calls(
        self, call: Call, delegations: Dict[str, set], token_proxies: Dict[str, dict]
    ) -> ABISubmoduleAbc.decode:
        """ Decode calls. """
        ...

    @abstractmethod
    def decode_events(
        self,
        events: [Event],
        delegations: Dict[str, set],
        token_proxies: Dict[str, dict],
    ) -> ABISubmoduleAbc.decode:
        """ Decode events. """
        ...

    @abstractmethod
    def decode_transfers(
        self, call: DecodedCall, events, token_proxies
    ) -> ABISubmoduleAbc.decode:
        """ Decode transfers. """
        ...

    @abstractmethod
    def decode_balances(
        self, transfers: List[DecodedTransfer]
    ) -> ABISubmoduleAbc.decode:
        """ Decode balances. """
        ...
