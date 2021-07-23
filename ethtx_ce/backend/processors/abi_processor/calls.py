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

from typing import Optional, Dict

from ethtx_ce.helpers import RecursionLimit
from .abc import ABISubmoduleAbc
from ..decoders.parameters import decode_function_parameters, decode_graffiti_parameters
from ...models.decoded_model import DecodedCall
from ...models.objects_model import Call

RECURSION_LIMIT = 2000


class ABICallsDecoder(ABISubmoduleAbc):
    """ Abi Calls Decoder. """

    def decode(
        self, call: Call, delegations: Dict[str, set], token_proxies: Dict[str, dict]
    ) -> Optional[DecodedCall]:
        """ Decode call with sub_calls. """

        if not call:
            return None

        indent = 0
        status = True
        call_id = ""
        decoded_root_call = self.decode_call(
            call, call_id, indent, status, delegations, token_proxies
        )

        with RecursionLimit(RECURSION_LIMIT):
            return self._decode_nested_calls(
                decoded_root_call,
                call.subcalls,
                indent,
                status,
                delegations,
                token_proxies,
            )

    def decode_call(
        self,
        call: Call,
        call_id: str = "",
        indent: int = 0,
        status: bool = True,
        delegations: Dict[str, set] = None,
        token_proxies: Dict[str, dict] = None,
    ) -> DecodedCall:
        """ Decode single call. """
        if call.call_data:
            function_signature = call.call_data[:10]
        else:
            function_signature = None

        from_name = self.repository.get_address_label(
            call.chain_id, call.from_address, token_proxies
        )
        to_name = self.repository.get_address_label(
            call.chain_id, call.to_address, token_proxies
        )

        if call.call_type == "selfdestruct":
            function_name = call.call_type
            function_input, function_output = [], []
        elif call.call_type == "create2":
            # constructor_abi = self.repository.get_constructor_abi(call.chain_id, call.to_address)
            function_name = "new"
            function_input, function_output = [], []
        elif self.repository.check_is_contract(call.chain_id, call.to_address):

            function_abi = self.repository.get_function_abi(
                call.chain_id, call.to_address, function_signature
            )
            if not function_abi and call.to_address in delegations:
                # try to find signature in delegate-called contracts
                for delegate in delegations[call.to_address]:
                    function_abi = self.repository.get_function_abi(
                        call.chain_id, delegate, function_signature
                    )
                    if function_abi:
                        break

            function_name = function_abi.name if function_abi else function_signature
            function_input, function_output = decode_function_parameters(
                call.call_data, call.return_value, function_abi, call.status
            )
            if (
                not call.status
                and function_output
                and function_output[0].name == "Error"
            ):
                error_description = function_output.pop()
                call.error = f'Failed with "{error_description.value}"'
        else:
            function_name = "fallback"
            function_input = decode_graffiti_parameters(call.call_data)
            function_output = []

        return DecodedCall(
            chain_id=call.chain_id,
            tx_hash=call.tx_hash,
            call_id=call_id,
            call_type=call.call_type,
            from_address=call.from_address,
            from_name=from_name,
            to_address=call.to_address,
            to_name=to_name,
            value=call.call_value / 10 ** 18,
            function_signature=function_signature,
            function_name=function_name,
            arguments=function_input,
            outputs=function_output,
            gas_used=call.gas_used,
            error=call.error,
            status=status,
            indent=indent,
        )

    def _decode_nested_calls(
        self, call: DecodedCall, sub_calls, indent, status, delegations, token_proxies
    ) -> DecodedCall:
        """ Decode nested calls. Call may have sub_calls, if they exist, it will recursively prcoess them."""
        for i, sub_call in enumerate(sub_calls):
            status = status and call.status

            sub_call_id = (
                "_".join([call.call_id, str(i).zfill(4)]) if call.call_id else str(i)
            )
            decoded = self.decode_call(
                sub_call, sub_call_id, indent + 1, status, delegations, token_proxies
            )
            call.sub_calls.append(decoded)

            if sub_call.subcalls:
                self._decode_nested_calls(
                    decoded,
                    sub_call.subcalls,
                    indent + 1,
                    status,
                    delegations,
                    token_proxies,
                )

        return call
