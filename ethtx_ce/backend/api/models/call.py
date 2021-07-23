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


class PayloadCall:
    """ POST Call Payload. """

    tx_hash: str
    chain_id: str
    from_address: str
    to_address: str
    call_value: int
    call_type: str
    call_data: str
    gas_used: int
    error: str
    status: bool

    subcalls: List

    def __init__(
        self,
        type: str,
        from_address: str,
        tx_hash: str,
        to_address: str,
        input: str,
        output: Optional[str],
        gas_used: str,
        chain_id: str,
        error: Optional[str],
        status: bool,
        value: Optional[str],
        subcalls: Optional[List] = None,
    ):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.call_type = type.lower()
        self.from_address = from_address
        self.to_address = to_address
        self.call_value = int(value, 16) if value else 0
        self.call_data = input
        self.return_value = output
        self.gas_used = int(gas_used, 16) if gas_used else None
        self.error = error
        self.status = status
        self.subcalls = subcalls if subcalls else []


class PayloadDecodeCall:
    """ Decoded call - call + transaction metadata. """

    tx_metadata: PayloadTransaction
    call: PayloadCall

    def __init__(self, tx_metadata: PayloadTransaction, call: PayloadCall):
        self.tx_metadata = tx_metadata
        self.call = call

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"(transaction="
            f"{jsonpickle.decode(jsonpickle.encode(self.tx_metadata, make_refs=False, unpicklable=False))},"
            f" call={jsonpickle.decode(jsonpickle.encode(self.call, make_refs=False, unpicklable=False))})>"
        )
