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

import logging

import requests
from flask import render_template, Blueprint, request, current_app, Response

from ethtx_ce.config import EthConfig
from . import route
from .deps import requires_auth

log = logging.getLogger(__name__)

bp = Blueprint("frontend", __name__)


@route(bp, "/")
def search_page() -> render_template:
    """ Render search page - index. """
    return render_template("index.html"), 200


@route(bp, "/terms")
def terms_page() -> render_template:
    """ Render terms page - terms. """
    return render_template("terms.html"), 200


@route(bp, "/privacy")
def privacy_page() -> render_template:
    """ Render privacy page - privacy. """
    return render_template("privacy.html"), 200


@route(bp, "/<string:chain_id>/<string:tx_hash>/", methods=["GET"])
def transaction_with_chain(tx_hash: str, chain_id: str) -> "show_transaction_page":
    """ Transaction with hash and chain. """
    response = requests.get(
        f"{request.url_root}api/transactions/{chain_id}/{tx_hash}",
        headers={"x-api-key": current_app.config["API_KEY"]},
    )
    return show_transaction_page(response)


@route(bp, "/<string:tx_hash>/", methods=["GET"])
def transaction(tx_hash: str) -> "show_transaction_page":
    """ Transaction with hash. """
    response = requests.get(
        f"{request.url_root}api/transactions/{EthConfig.DEFAULT_CHAIN}/{tx_hash}",
        headers={"x-api-key": current_app.config["API_KEY"]},
    )
    return show_transaction_page(response)


def show_transaction_page(response: Response) -> render_template:
    """ Render transaction/exception page. """
    status_code = response.status_code
    req_response = response.json()

    if status_code == 200:
        return (
            render_template(
                "transaction.html",
                transaction=req_response["tx_metadata"],
                events=req_response["events"],
                call=req_response["calls"],
                transfers=req_response["transfers"],
                balances=req_response["balances"],
            ),
            200,
        )

    log.error(
        "Could not render transaction page. Status code: %d. Response: %s",
        status_code,
        req_response,
    )
    return (
        render_template("exception.html", exception=req_response.get("error", "")),
        status_code,
    )


@route(bp, "/semantics/<string:chain_id>/<string:address>/", methods=["GET"])
def semantics_with_chain(address: str, chain_id: str) -> "show_semantics_page":
    """ Semantics of address on a chain. """
    response = requests.get(
        f"{request.url_root}api/semantics/{chain_id}/{address}",
        headers={"x-api-key": current_app.config["API_KEY"]},
    )
    return show_semantics_page(response)


@route(bp, "/semantics/<string:address>/", methods=["GET"])
def semantics(address: str) -> "show_semantics_page":
    """ Semantics of address. """
    response = requests.get(
        f"{request.url_root}api/semantics/{EthConfig.DEFAULT_CHAIN}/{address}",
        headers={"x-api-key": current_app.config["API_KEY"]},
    )
    return show_semantics_page(response)


@requires_auth
def show_semantics_page(response: Response) -> render_template:
    """ Render semantics editor page. """
    status_code = response.status_code
    req_response = response.json()

    if status_code == 200 and req_response:
        address = req_response.get("address")
        chain_id = req_response.get("chain_id", EthConfig.DEFAULT_CHAIN)
        name = req_response.get("name", address)

        if req_response.get("is_contract", False):
            events = req_response["contract"].get("events", {})
            functions = req_response["contract"].get("functions", {})
            transformations = req_response["contract"].get("transformations", {})
            code_hash = req_response["contract"].get("code_hash")
            contract_name = req_response["contract"].get("name")
        else:
            events = {}
            functions = {}
            transformations = {}
            code_hash = "EOA"
            contract_name = address

        standard = req_response.get("standard")
        # ToDo: make it more universal

        if standard == "ERC20":
            standard_info = req_response.get("erc20", {})
        elif standard == "ERC721":
            standard_info = req_response.get("erc721", {})
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

    log.error(
        "Could not render semantics page. Status code: %d. Response: %s",
        status_code,
        req_response,
    )
    return (
        render_template("exception.html", exception=req_response.get("error", "")),
        status_code,
    )
