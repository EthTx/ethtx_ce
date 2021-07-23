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

from typing import List, Dict, Union


from .abc import ABISubmoduleAbc
from ..decoders.parameters import decode_event_parameters
from ...models.decoded_model import DecodedEvent
from ...models.objects_model import Event
from ethtx_ce.semantics.standards.erc20 import ERC20_EVENTS


class ABIEventsDecoder(ABISubmoduleAbc):
    """ Abi Events Decoder. """

    def decode(
        self,
        events: Union[Event, List[Event]],
        delegations: Dict[str, set],
        token_proxies: Dict[str, dict],
    ) -> Union[DecodedEvent, List[DecodedEvent]]:
        """ Return list of decoded events. """
        if isinstance(events, list):
            return (
                [
                    self.decode_event(event, delegations, token_proxies)
                    for event in events
                ]
                if events
                else []
            )

        return self.decode_event(events, delegations, token_proxies)

    def decode_event(
        self, event: Event, delegations: Dict[str, set], token_proxies: Dict[str, dict]
    ) -> DecodedEvent:
        """ Decode single event. """

        if event.topics:
            event_signature = event.topics[0]
        else:
            event_signature = None

        anonymous = False

        event_abi = self.repository.get_event_abi(
            event.chain_id, event.contract, event_signature
        )

        if not event_abi:

            if event_signature in ERC20_EVENTS:
                # try standard ERC20 events
                event_abi = ERC20_EVENTS[event_signature]

            if not event_abi:
                # if signature is not known but there is exactly one anonymous event in tha ABI
                # we can assume that this is this the anonymous one (e.g. Maker's LogNote)
                event_abi = self.repository.get_anonymous_event_abi(
                    event.chain_id, event.contract
                )
                if event_abi:
                    anonymous = True

            if not event_abi and event.contract in delegations:
                # try to find signature in delegate-called contracts
                for delegate in delegations[event.contract]:
                    event_abi = self.repository.get_event_abi(
                        event.chain_id, delegate, event_signature
                    )
                    if event_abi:
                        break

        contract_name = self.repository.get_address_label(
            event.chain_id, event.contract, token_proxies
        )
        event_name = event_abi.name if event_abi else event_signature
        parameters = decode_event_parameters(
            event.log_data, event.topics, event_abi, anonymous
        )

        return DecodedEvent(
            chain_id=event.chain_id,
            tx_hash=event.tx_hash,
            contract_address=event.contract,
            contract_name=contract_name,
            index=event.log_index,
            event_signature=event_signature,
            event_name=event_name,
            parameters=parameters,
        )
