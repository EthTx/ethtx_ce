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

import json
import logging
from typing import Optional, List, Dict

from ethtx import EthTx
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
from web3 import Web3

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


@frontend_route(bp, "/reload", methods=["POST"])
@auth.login_required
def reload_semantics():
    """Reload raw semantic."""
    data = json.loads(request.data)

    ethtx: EthTx = current_app.ethtx
    ethtx.semantics.database._addresses.delete_one({"address": data["address"]})
    ethtx.semantics.get_semantics.cache_clear()
    ethtx.semantics.get_semantics(
        data["chain_id"] if data.get("chain_id") else current_app.ethtx._default_chain,
        data["address"],
    )

    return "ok"


@frontend_route(bp, "/save", methods=["POST"])
@auth.login_required
def semantics_save():
    data = json.loads(request.data)
    return _semantics_save(data)


@frontend_route(bp, "/poke", methods=["POST"])
@auth.login_required
def poke_abi():
    data = json.loads(request.data)
    return _poke_abi(data)


def show_semantics_page(data: AddressSemantics) -> render_template:
    if data:

        data_dict = data.dict()

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


def _parameters_semantics(parameters: List[Dict]) -> List[ParameterSemantics]:
    parameters_semantics_list = []
    if parameters:
        for parameter in parameters:
            parameters_semantics_list.append(
                ParameterSemantics(
                    parameter_name=parameter.get("parameter_name"),
                    parameter_type=parameter.get("parameter_type"),
                    components=parameter.get("components", []),
                    indexed=parameter.get("indexed", False),
                    dynamic=parameter.get("dynamic", False),
                )
            )

    return parameters_semantics_list


def _semantics_save(data):
    try:
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
                    parameters=_parameters_semantics(event.get("parameters")),
                )

            for function in functions.values():
                functions_semantics[function.get("signature")] = FunctionSemantics(
                    signature=function.get("signature"),
                    name=function.get("name"),
                    inputs=_parameters_semantics(function.get("inputs")),
                    outputs=_parameters_semantics(function.get("outputs")),
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


def _poke_abi(data):
    # helper function decoding contract ABI
    def _parse_abi(json_abi):

        # helper function to recursively parse parameters
        def _parse_parameters(parameters):

            comp_canonical = "("
            comp_inputs = list()

            for i, parameter in enumerate(parameters):
                argument = dict(
                    parameter_name=parameter["name"], parameter_type=parameter["type"]
                )

                if parameter["type"][:5] == "tuple":
                    sub_canonical, sub_components = _parse_parameters(
                        parameter["components"]
                    )
                    comp_canonical += sub_canonical + parameter["type"][5:]
                    argument["components"] = sub_components
                else:
                    comp_canonical += parameter["type"]
                    sub_components = []

                if i < len(parameters) - 1:
                    comp_canonical += ","

                if (
                    parameter["type"] in ("string", "bytes")
                    or parameter["type"][-2:] == "[]"
                ):
                    argument["dynamic"] = True
                elif parameter["type"] == "tuple":
                    argument["dynamic"] = any(c["dynamic"] for c in sub_components)
                else:
                    argument["dynamic"] = False

                if "indexed" in parameter:
                    argument["indexed"] = parameter["indexed"]

                comp_inputs.append(argument)

            comp_canonical += ")"

            return comp_canonical, comp_inputs

        functions = dict()
        events = dict()

        for item in json_abi:
            if "type" in item:

                # parse contract functions
                if item["type"] == "constructor":
                    _, inputs = _parse_parameters(item["inputs"])
                    functions["constructor"] = dict(
                        signature="constructor",
                        name="constructor",
                        inputs=inputs,
                        outputs=[],
                    )
                elif item["type"] == "fallback":
                    functions["fallback"] = {}

                elif item["type"] == "function":
                    canonical, inputs = _parse_parameters(item["inputs"])
                    canonical = item["name"] + canonical
                    function_hash = Web3.sha3(text=canonical).hex()
                    signature = function_hash[0:10]

                    _, outputs = _parse_parameters(item["outputs"])

                    functions[signature] = dict(
                        signature=signature,
                        name=item["name"],
                        inputs=inputs,
                        outputs=outputs,
                    )

                # parse contract events
                elif item["type"] == "event":
                    canonical, parameters = _parse_parameters(item["inputs"])
                    canonical = item["name"] + canonical
                    event_hash = Web3.sha3(text=canonical).hex()
                    signature = event_hash

                    events[signature] = dict(
                        signature=signature,
                        name=item["name"],
                        anonymous=item["anonymous"],
                        parameters=parameters,
                    )

        return functions, events

    try:

        address = data["address"]
        chash = data["chash"]
        network = data["network"]
        name = data["name"]
        standard = json.loads(data["standard"])
        abi = json.loads(data["abi"])

        if abi and abi != []:

            is_contract = True
            functions, events = _parse_abi(abi)

            events_semantics = dict()
            for event in events.values():
                events_semantics[event.get("signature")] = EventSemantics(
                    signature=event.get("signature"),
                    anonymous=event.get("anonymous"),
                    name=event.get("name"),
                    parameters=_parameters_semantics(event.get("parameters")),
                )

            functions_semantics = dict()
            for function in functions.values():
                functions_semantics[function.get("signature")] = FunctionSemantics(
                    signature=function.get("signature"),
                    name=function.get("name"),
                    inputs=_parameters_semantics(function.get("inputs")),
                    outputs=_parameters_semantics(function.get("outputs")),
                )

            contract_semantics = ContractSemantics(
                code_hash=chash,
                name=name,
                events=events_semantics,
                functions=functions_semantics,
                transformations=dict(),
            )

        else:

            is_contract = False
            contract_semantics = ContractSemantics(
                code_hash="0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470",
                name="EOA",
                events=dict(),
                functions=dict(),
                transformations=dict(),
            )

        address_semantics = AddressSemantics(
            chain_id=network,
            address=address,
            name=name,
            is_contract=is_contract,
            contract=contract_semantics,
            standard=standard.get("name"),
            erc20=ERC20Semantics(
                name=standard["data"].get("name"),
                symbol=standard["data"].get("symbol"),
                decimals=standard["data"].get("decimals"),
            )
            if standard.get("name") == "ERC20"
            else None,
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

        logging.info(f"ABI for {address} decoded.")

        result = "ok"

    except Exception as e:
        logging.exception("ABI retrieval error: %s" % e)
        result = "error"

    return jsonify(result=result)
