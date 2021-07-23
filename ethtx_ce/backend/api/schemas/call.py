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

from typing import NoReturn, Union, Dict

from marshmallow import Schema, fields, pre_load, ValidationError, post_dump

from ..schemas import PayloadTransactionSchema


class PayloadCallSchema(Schema):
    """ POST Call Payload Schema. """

    from_address = fields.String(required=True)
    to_address = fields.String(required=True)
    value = fields.String(required=False)
    type = fields.String(required=True)
    input = fields.String(required=True)
    output = fields.String(required=False)
    gas_used = fields.String(required=False)
    error = fields.String(required=False)
    status = fields.Boolean(required=True)

    subcalls = fields.List(fields.Raw(), required=False, default=[])


class PayloadDecodeCallSchema(Schema):
    """ Decode call - call + transaction metadata. """

    transaction = fields.Nested(PayloadTransactionSchema)
    call = fields.Nested(PayloadCallSchema)

    @pre_load
    def validate_schema(self, data, many, **_) -> Union[NoReturn, Dict]:
        """ Validate input data type. """
        if isinstance(data, list) and not many:
            raise ValidationError(
                "Multiple Calls decoding not allowed. Use /decoders/calls/bulk endpoint."
            )

        return data

    @post_dump
    def update_schema(self, data, **_) -> Dict:
        """ Update call schema. Inherit chain_id and tx_hash from transaction. """
        data["call"]["chain_id"] = data["transaction"]["chain_id"]
        data["call"]["tx_hash"] = data["transaction"]["tx_hash"]

        return data
