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

# TODO: move it to pro version
"""@decoders_ns.route("/calls")
@decoders_ns.hide
class CallResource(Resource):

    decorators = [auth_required]

    @decoders_ns.doc("Decode Call")
    @response(200)
    def post(self):
        data = request.json

        decode_schema = PayloadDecodeCallSchema(many=False)
        errors = decode_schema.validate(data)

        if errors:
            raise MalformedRequest(errors)

        dump_data = decode_schema.dump(data)

        transaction = PayloadTransaction(**dump_data["transaction"])
        call = PayloadCall(**dump_data["call"])

        decoded = DecoderService.decode_call(call=call, transaction=transaction)

        return decoded


@decoders_ns.route("/calls/_bulk")
@decoders_ns.hide
class BulkCallResource(Resource):

    decorators = [auth_required]

    @decoders_ns.doc("Decode array of Calls")
    @limit_content_length
    @response(200)
    def post(self):
        decoded = []
        data = request.json

        decode_schema = PayloadDecodeCallSchema(many=True)
        errors = decode_schema.validate(data, many=True)

        if errors:
            raise MalformedRequest(errors)

        dump_data_set = decode_schema.dump(data)

        for dump_data in dump_data_set:
            transaction = PayloadTransaction(**dump_data["transaction"])

            call = PayloadCall(**dump_data["call"])

            try:
                decoded.append(
                    DecoderService.decode_call(call=call, transaction=transaction)
                )
            except Exception as e:
                decoded.append({"error": str(e)})

        return decoded


@decoders_ns.route("/events")
@decoders_ns.hide
class EventResource(Resource):

    decorators = [auth_required]

    @decoders_ns.doc("Decode Event")
    @response(200)
    def post(self):
        data = request.json

        decode_schema = PayloadDecodeEventSchema(many=False)
        errors = decode_schema.validate(data)

        if errors:
            raise MalformedRequest(errors)

        dump_data = decode_schema.dump(data)

        transaction = PayloadTransaction(**dump_data["transaction"])
        event = PayloadEvent(**dump_data["event"])

        decoded = DecoderService.decode_event(event=event, transaction=transaction)

        return decoded


@decoders_ns.route("/events/_bulk")
@decoders_ns.hide
class BulkEventResource(Resource):

    decorators = [auth_required]

    @decoders_ns.doc("Decode array of Events")
    @limit_content_length
    @response(200)
    def post(self):
        decoded = []
        data = request.json

        decode_schema = PayloadDecodeEventSchema(many=True)
        errors = decode_schema.validate(data, many=True)

        if errors:
            raise MalformedRequest(errors)

        dump_data_set = decode_schema.dump(data)

        for dump_data in dump_data_set:
            transaction = PayloadTransaction(**dump_data["transaction"])
            event = PayloadEvent(**dump_data["event"])

            try:
                decoded.append(
                    DecoderService.decode_event(event=event, transaction=transaction)
                )
            except Exception as e:
                decoded.append({"error": str(e)})

        return decoded
"""
