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
from typing import Any, List

from ...models.decoded_model import (
    DecodedTransfer,
    DecodedCall,
    TransactionMetadata,
    DecodedBalance,
    DecodedEvent,
    FullDecodedTransaction,
)
from ...providers.semantic_providers.semantics_repository import SemanticsRepository


class SemanticSubmoduleAbc(ABC):
    """ Semantic submodule properties. """

    def __init__(self, repository: SemanticsRepository):
        self.repository = repository

    @abstractmethod
    def decode(self, *args, **kwargs) -> Any:
        """ Return decoded object. """
        raise NotImplementedError


class SemanticProcessorAbc(ABC):
    """ Semantic Processor - abstract. Base class."""

    def __init__(self, repository: SemanticsRepository):
        self.repository = repository

    @abstractmethod
    def decode_with_semantics(
        self, transaction: FullDecodedTransaction
    ) -> FullDecodedTransaction:
        """ Decode with semantics. """

    @abstractmethod
    def decode_metadata(self, tx_metadata: TransactionMetadata):
        """ Semantically decode metadata. """
        raise NotImplementedError

    @abstractmethod
    def decode_calls(
        self, call: DecodedCall, tx_metadata: TransactionMetadata
    ) -> SemanticSubmoduleAbc.decode:
        """ Semantically decode calls. """
        raise NotImplementedError

    @abstractmethod
    def decode_events(
        self, events: List[DecodedEvent], tx_metadata: TransactionMetadata
    ) -> SemanticSubmoduleAbc.decode:
        """ Semantically decode events. """
        raise NotImplementedError

    @abstractmethod
    def decode_transfers(
        self, transfers: List[DecodedTransfer]
    ) -> SemanticSubmoduleAbc.decode:
        """" Semantically decode transfers. """
        raise NotImplementedError

    @abstractmethod
    def decode_balances(
        self, balances: List[DecodedBalance]
    ) -> SemanticSubmoduleAbc.decode:
        """ Semantically decode balances. """
        raise NotImplementedError
