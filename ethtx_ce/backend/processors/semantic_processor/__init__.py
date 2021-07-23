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

from typing import List

from .abc import SemanticProcessorAbc
from .balances import SemanticBalancesDecoder
from .calls import SemanticCallsDecoder
from .events import SemanticEventsDecoder
from .metadata import SemanticMetadataDecoder
from .transfers import SemanticTransfersDecoder
from ...models.decoded_model import (
    FullDecodedTransaction,
    TransactionMetadata,
    DecodedCall,
    DecodedEvent,
    DecodedTransfer,
    DecodedBalance,
)


class SemanticProcessor(SemanticProcessorAbc):
    """ Semantic Processor. Decode full or part of the transaction. """

    def decode_with_semantics(
        self, transaction: FullDecodedTransaction
    ) -> FullDecodedTransaction:
        """ Semantically decode full transaction. """
        self.decode_metadata(transaction.tx_metadata)
        self.decode_events(transaction.events, transaction.tx_metadata)
        self.decode_calls(transaction.calls, transaction.tx_metadata)
        self.decode_transfers(transaction.transfers)
        self.decode_balances(transaction.balances)

        return transaction

    def decode_metadata(self, tx_metadata: TransactionMetadata):
        """ Semantically decode metadata. """
        return SemanticMetadataDecoder(repository=self.repository).decode(
            tx_metadata=tx_metadata
        )

    def decode_calls(self, call: DecodedCall, tx_metadata: TransactionMetadata):
        """ Semantically decode calls. """
        return SemanticCallsDecoder(repository=self.repository).decode(
            call=call, tx_metadata=tx_metadata
        )

    def decode_events(
        self, events: List[DecodedEvent], tx_metadata: TransactionMetadata
    ):
        """ Semantically decode events. """
        return SemanticEventsDecoder(repository=self.repository).decode(
            events=events, tx_metadata=tx_metadata
        )

    def decode_transfers(self, transfers: List[DecodedTransfer]):
        """ Semantically decode transfers. """
        return SemanticTransfersDecoder(repository=self.repository).decode(
            transfers=transfers
        )

    def decode_balances(self, balances: List[DecodedBalance]):
        """ Semantically decode balances. """
        return SemanticBalancesDecoder(repository=self.repository).decode(
            balances=balances
        )
