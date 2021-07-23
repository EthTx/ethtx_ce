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
import traceback
from datetime import datetime
from typing import Optional, Dict, List

from .abc import ABIProcessorAbc
from .balances import ABIBalancesDecoder
from .calls import ABICallsDecoder
from .events import ABIEventsDecoder
from .transfers import ABITransfersDecoder
from ...models.decoded_model import (
    FullDecodedTransaction,
    DecodedCall,
    DecodedEvent,
    DecodedTransfer,
    TransactionMetadata,
)
from ...models.objects_model import FullTransaction, Call, Event

log = logging.getLogger(__name__)


class ABIProcessor(ABIProcessorAbc):
    """ Abi Processor. Decode full or part of the transaction. """

    def decode_with_abi(
        self, transaction: FullTransaction
    ) -> Optional[FullDecodedTransaction]:
        start_timestamp = datetime.now()
        log.info("ABI decoding for %s / %s.", transaction.tx_hash, transaction.chain_id)

        try:
            full_decoded_transaction = self._decode_transaction(transaction)
            end_timestamp = datetime.now()
            log.info(
                "Processing time: %s s.",
                (end_timestamp - start_timestamp).total_seconds(),
            )
            return full_decoded_transaction
        except Exception as e:
            log.warning(
                "ABI decoding of %s / %s failed.",
                transaction.tx_hash,
                transaction.chain_id,
            )
            traceback.print_exc(e)

        return None

    def decode_calls(
        self, call: Call, delegations: Dict[str, set], token_proxies: Dict[str, dict]
    ) -> Optional[DecodedCall]:
        """ Decode calls. """
        return ABICallsDecoder(repository=self.repository).decode(
            call=call, delegations=delegations, token_proxies=token_proxies
        )

    def decode_events(
        self,
        events: [Event],
        delegations: Dict[str, set],
        token_proxies: Dict[str, dict],
    ) -> List[DecodedEvent]:
        """ Decode events. """

        return ABIEventsDecoder(repository=self.repository).decode(
            events=events, delegations=delegations, token_proxies=token_proxies
        )

    def decode_transfers(self, call: DecodedCall, events, token_proxies):
        """ Decode transfers. """

        return ABITransfersDecoder(repository=self.repository).decode(
            call=call, events=events, token_proxies=token_proxies
        )

    def decode_balances(self, transfers: List[DecodedTransfer]):
        """ Decode balances. """

        return ABIBalancesDecoder(repository=self.repository).decode(
            transfers=transfers
        )

    def _decode_transaction(self, transaction: FullTransaction):
        """ Decode transaction and catch exceptions. """
        tx_metadata = TransactionMetadata(
            chain_id=transaction.chain_id,
            block_number=transaction.block.block_number,
            timestamp=transaction.block.timestamp,
            tx_hash=transaction.tx_hash,
            sender=transaction.transaction.from_address,
            receiver=transaction.transaction.to_address,
            gas_used=transaction.transaction.gas_used,
            gas_price=transaction.transaction.gas_price,
        )

        full_decoded_transaction = FullDecodedTransaction(
            tx_metadata=tx_metadata, events=[], calls=None, transfers=[], balances=[]
        )

        # prepare lists of delegations to properly decode delegate-calling contracts
        delegations = self.get_delegations(transaction.root_call)
        token_proxies = self.get_token_proxies(delegations, tx_metadata)

        try:
            full_decoded_transaction.calls = self.decode_calls(
                transaction.root_call, delegations, token_proxies
            )
        except Exception as e:
            log.warning(
                "ABI decoding of calls tree for %s / %s failed.",
                transaction.tx_hash,
                transaction.chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        try:
            full_decoded_transaction.events = self.decode_events(
                transaction.events, delegations, token_proxies
            )
        except Exception as e:
            log.warning(
                "ABI decoding of events for %s / %s failed.",
                transaction.tx_hash,
                transaction.chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        try:
            full_decoded_transaction.transfers = self.decode_transfers(
                full_decoded_transaction.calls,
                full_decoded_transaction.events,
                token_proxies,
            )
        except Exception as e:
            log.warning(
                "ABI decoding of transfers for %s / %s failed.",
                transaction.tx_hash,
                transaction.chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        try:
            full_decoded_transaction.balances = self.decode_balances(
                full_decoded_transaction.transfers
            )
        except Exception as e:
            log.warning(
                "ABI decoding of balances for %s / %s failed.",
                transaction.tx_hash,
                transaction.chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        full_decoded_transaction.status = True

        return full_decoded_transaction
