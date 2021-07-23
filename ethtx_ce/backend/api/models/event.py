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

from typing import Optional, List

import jsonpickle

from .transaction import PayloadTransaction


class PayloadEvent:
    """ POST Event Payload. """

    chain_id: str
    tx_hash: str
    contract: str
    topic: List[str]
    log_data: Optional[str]
    log_index: int

    def __init__(
        self,
        chain_id: str,
        tx_hash: str,
        contract: str,
        log_index: int,
        log_data: Optional[str] = "",
        topics: Optional[List[str]] = None,
    ):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.contract = contract
        self.topics = topics if topics else []
        self.log_index = log_index
        self.log_data = log_data


class PayloadDecodeEvent:
    """ Decoded event - event + transaction metadata. """

    tx_metadata: PayloadTransaction
    event: PayloadEvent

    def __init__(self, tx_metadata: PayloadTransaction, event: PayloadEvent):
        self.tx_metadata = tx_metadata
        self.event = event

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"(transaction="
            f"{jsonpickle.decode(jsonpickle.encode(self.tx_metadata, make_refs=False, unpicklable=False))},"
            f" call={jsonpickle.decode(jsonpickle.encode(self.event, make_refs=False, unpicklable=False))})>"
        )
