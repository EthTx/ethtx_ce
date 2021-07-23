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

from ethtx_ce.backend import eth_tx_processor, semantics_db
from ethtx_ce.backend.api.models import PayloadCall, PayloadTransaction, PayloadEvent

from ethtx_ce.backend.models.decoded_model import (
    FullDecodedTransaction,
    DecodedCall,
    DecodedEvent,
)
from ethtx_ce.backend.models.objects_model import FullTransaction
from ethtx_ce.backend.models.semantics_model import AddressSemantics
from ethtx_ce.backend.validators import assert_tx_hash_is_correct


class DecoderService:
    """ Decoder Service. """

    abi_processor = eth_tx_processor.abi_processor
    semantic_processor = eth_tx_processor.semantic_processor
    semantic = semantics_db

    @classmethod
    def decode_transaction(cls, chain_id: str, tx_hash: str) -> FullDecodedTransaction:
        """ Decode full transaction. """
        assert_tx_hash_is_correct(tx_hash)
        raw_tx = FullTransaction(tx_hash=tx_hash, chain_id=chain_id)
        abi_decoded_tx = cls.abi_processor.decode_with_abi(transaction=raw_tx)
        semantically_decoded_tx = cls.semantic_processor.decode_with_semantics(
            abi_decoded_tx
        )

        return semantically_decoded_tx

    @classmethod
    def decode_call(
        cls, call: PayloadCall, transaction: PayloadTransaction
    ) -> DecodedCall:
        """ Decode call. """
        delegations = cls.abi_processor.get_delegations(call)
        token_proxies = cls.abi_processor.get_token_proxies(delegations, transaction)
        decoded_call_with_abi = cls.abi_processor.decode_calls(
            call, delegations, token_proxies
        )
        decoded_call_with_semantic = cls.semantic_processor.decode_calls(
            decoded_call_with_abi, transaction
        )

        return decoded_call_with_semantic

    @classmethod
    def decode_event(
        cls, event: PayloadEvent, transaction: PayloadTransaction
    ) -> DecodedEvent:
        """ Decode event. """
        decode_event_with_abi = cls.abi_processor.decode_events(event, {}, {})
        decoded_event_with_semantic = cls.semantic_processor.decode_events(
            decode_event_with_abi, transaction
        )

        return decoded_event_with_semantic

    @classmethod
    def decode_semantic(cls, chain_id: str, address: str) -> AddressSemantics:
        """ Get raw semantic. """
        raw_semantic = cls.semantic.db.get_raw_semantics(
            chain_id=chain_id, address=address
        )

        return raw_semantic
