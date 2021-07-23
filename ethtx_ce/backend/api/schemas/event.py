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

from .transaction import PayloadTransactionSchema


class PayloadEventSchema(Schema):
    """ POST Event Payload Schema. """

    contract = fields.String(required=True)
    log_index = fields.Integer(required=True)
    log_data = fields.String(required=False)
    topics = fields.List(fields.String(), required=False)


class PayloadDecodeEventSchema(Schema):
    """ Decode event - event + transaction metadata. """

    transaction = fields.Nested(PayloadTransactionSchema)
    event = fields.Nested(PayloadEventSchema)

    @pre_load
    def validate_schema(self, data, many, **_) -> Union[NoReturn, Dict]:
        """ Validate input data type. """
        if isinstance(data, list) and not many:
            raise ValidationError(
                "Multiple Events decoding not allowed. Use /decoders/events/bulk endpoint."
            )

        return data

    @post_dump
    def update_schema(self, data, **_) -> Dict:
        """ Update event schema. Inherit chain_id and tx_hash from transaction. """
        data["event"]["chain_id"] = data["transaction"]["chain_id"]
        data["event"]["tx_hash"] = data["transaction"]["tx_hash"]

        return data
