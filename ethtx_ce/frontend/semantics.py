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

from __future__ import annotations

import logging
import json
from typing import Optional, List, Dict

from ethtx.models.semantics_model import (
    AddressSemantics,
    ContractSemantics,
    ERC20Semantics,
)
from ethtx.models.semantics_model import (
    EventSemantics,
    FunctionSemantics,
    TransformationSemantics,
    ParameterSemantics,
)
from flask import Blueprint, render_template, current_app, request, jsonify

from . import frontend_route
from .deps import auth
from ..exceptions import EmptyResponseError

bp = Blueprint("semantics", __name__)

log = logging.getLogger(__name__)


@frontend_route(bp, "/semantics/<string:address>/")
@frontend_route(bp, "/semantics/<string:chain_id>/<string:address>/")
@auth.login_required
def semantics(address: str, chain_id: Optional[str] = None) -> show_semantics_page:
    raw_semantics = current_app.ethtx.semantics.get_semantics(
        chain_id=chain_id or current_app.ethtx._default_chain, address=address
    )

    return show_semantics_page(raw_semantics)


@frontend_route(bp, "/save", methods=["POST"])
@auth.login_required
def semantics_save():
    def parameters_semantics(parameters: List[Dict]) -> List[ParameterSemantics]:
        parameters_semantics_list = []
        if parameters:
            for parameter in parameters:
                parameters_semantics_list.append(
                    ParameterSemantics(
                        parameter_name=parameter.get("parameter_name"),
                        parameter_type=parameter.get("parameter_type"),
                        components=parameter.get("components"),
                        indexed=parameter.get("indexed"),
                        dynamic=parameter.get("dynamic"),
                    )
                )

        return parameters_semantics_list

    try:
        data = json.loads(request.data)
        address = data.get("address")
        metadata = data.get("metadata")
        events = data.get("events")
        functions = data.get("functions")
        transformations = data.get("transformations")
        standard_name = None
        erc20_semantics = None

        if metadata.get("contract"):

            events_semantics = dict()
            functions_semantics = dict()
            transformations_semantics = dict()

            for event in events.values():
                events_semantics[event.get("signature")] = EventSemantics(
                    signature=event.get("signature"),
                    anonymous=event.get("anonymous"),
                    name=event.get("name"),
                    parameters=parameters_semantics(event.get("parameters")),
                )

            for function in functions.values():
                functions_semantics[function.get("signature")] = FunctionSemantics(
                    signature=function.get("signature"),
                    name=function.get("name"),
                    inputs=parameters_semantics(function.get("inputs")),
                    outputs=parameters_semantics(function.get("outputs")),
                )

            for signature, transformation in transformations.items():
                transformations_semantics[signature] = dict()
                for parameter_name, parameter_transformation in transformation:
                    transformations_semantics[signature][
                        parameter_name
                    ] = TransformationSemantics(
                        transformed_name=parameter_transformation.get(
                            "transformed_name"
                        ),
                        transformed_type=parameter_transformation.get(
                            "transformed_type"
                        ),
                        transformation=parameter_transformation.get("transformation"),
                    )

            standard_name = metadata["contract"]["standard"]["name"]
            if standard_name == "ERC20":
                erc20_data = metadata["contract"]["standard"].get("data")
                if erc20_data:
                    erc20_semantics = ERC20Semantics(
                        name=erc20_data.get("name"),
                        symbol=erc20_data.get("symbol"),
                        decimals=erc20_data.get("decimals"),
                    )

            contract_semantics = ContractSemantics(
                code_hash=metadata["contract"].get("code_hash"),
                name=metadata["contract"].get("name"),
                events=events_semantics,
                functions=functions_semantics,
                transformations=transformations_semantics,
            )

        else:
            contract_semantics = None

        address_semantics = AddressSemantics(
            chain_id=metadata.get("chain"),
            address=address,
            name=metadata.get("label"),
            is_contract=contract_semantics is not None,
            contract=contract_semantics,
            standard=standard_name,
            erc20=erc20_semantics,
        )

        current_app.ethtx.semantics.update_semantics(semantics=address_semantics)
        current_app.ethtx.semantics.get_semantics.cache_clear()
        current_app.ethtx.semantics.get_event_abi.cache_clear()
        current_app.ethtx.semantics.get_anonymous_event_abi.cache_clear()
        current_app.ethtx.semantics.get_transformations.cache_clear()
        current_app.ethtx.semantics.get_function_abi.cache_clear()
        current_app.ethtx.semantics.get_constructor_abi.cache_clear()
        current_app.ethtx.semantics.check_is_contract.cache_clear()
        current_app.ethtx.semantics.get_standard.cache_clear()

        result = "ok"

    except Exception as e:
        logging.exception("Semantics save error: %s" % e)
        result = "error"

    return jsonify(result=result)


# @frontend_route(bp, '/poke', methods=['POST'])
# @auth.login_required
# def poke_abi():
#     try:
#         data = json.loads(request.data)
#         address = data["address"]
#         network = data["network"]
#         name = data["name"]
#         abi = json.loads(data["abi"])
#         poke_abi(address, network, name, abi)
#         result = 'ok'
#
#     except Exception as e:
#         logging.exception('ABI retrieval error: %s' % e)
#         result = "error"
#
#     return jsonify(result=result)


def show_semantics_page(data: AddressSemantics) -> render_template:
    if data:

        data_dict = data.json()

        address = data.address
        chain_id = data.chain_id
        name = data.name or address

        if data.is_contract:
            events = data_dict["contract"]["events"] or {}
            functions = data_dict["contract"]["functions"] or {}
            transformations = data_dict["contract"]["transformations"] or {}
            code_hash = data.contract.code_hash
            contract_name = data.contract.name
        else:
            events = {}
            functions = {}
            transformations = {}
            code_hash = "EOA"
            contract_name = address

        standard = data.standard
        # ToDo: make it more universal

        if standard == "ERC20":
            standard_info = data_dict["erc20"] or {}
        elif standard == "ERC721":
            standard_info = {}
        else:
            standard_info = {}

        metadata = dict(
            label=name,
            chain=chain_id,
            contract=dict(
                name=contract_name,
                code_hash=code_hash,
                standard=dict(name=standard, data=standard_info),
            ),
        )

        return (
            render_template(
                "semantics.html",
                address=address,
                events=events,
                functions=functions,
                transformations=transformations,
                metadata=metadata,
            ),
            200,
        )

    raise EmptyResponseError(
        "The semantics are empty. It probably means that the given address "
        "has not been decoded before or address is incorrect."
    )
