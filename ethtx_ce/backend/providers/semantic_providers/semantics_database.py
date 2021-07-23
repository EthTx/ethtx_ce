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

from pymongo.database import Database

from ...models.semantics_model import (
    AddressSemantics,
    ContractSemantics,
    ERC20Semantics,
)
from ...models.semantics_model import (
    EventSemantics,
    FunctionSemantics,
    TransformationSemantics,
    ParameterSemantics,
)


class SemanticsDatabase:
    """ Semantics Database. """

    def __init__(self, db: Database):

        self._db = db
        self._addresses = self._db["addresses"]
        self._contracts = self._db["contracts"]
        self._signatures = self._db["signatures"]

    def get_raw_semantics(self, chain_id, address):
        def decode_parameter(parameter):

            components_semantics = []
            for component in parameter["components"]:
                components_semantics.append(decode_parameter(component))

            decoded_parameter = ParameterSemantics(
                parameter["parameter_name"],
                parameter["parameter_type"],
                components_semantics,
                parameter["indexed"],
                parameter["dynamic"],
            )

            return decoded_parameter

        ZERO_HASH = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"

        _id = f"{chain_id}-{address}"
        raw_address_semantics = self._addresses.find_one({"_id": _id}, {"_id": 0})
        if raw_address_semantics:

            if raw_address_semantics.get("erc20"):
                erc20_semantics = ERC20Semantics(
                    raw_address_semantics["erc20"]["name"],
                    raw_address_semantics["erc20"]["symbol"],
                    raw_address_semantics["erc20"]["decimals"],
                )
            else:
                erc20_semantics = None

            if raw_address_semantics["contract"] == ZERO_HASH:
                contract_semantics = ContractSemantics(
                    raw_address_semantics["contract"], "EOA", dict(), dict(), dict()
                )

            else:

                raw_contract_semantics = self._contracts.find_one(
                    {"_id": raw_address_semantics["contract"]}, {"_id": 0}
                )

                events = dict()
                for signature, event in raw_contract_semantics["events"].items():

                    parameters_semantics = []
                    for parameter in event["parameters"]:
                        parameters_semantics.append(decode_parameter(parameter))

                    events[signature] = EventSemantics(
                        signature,
                        event["anonymous"],
                        event["name"],
                        parameters_semantics,
                    )

                functions = dict()
                for signature, function in raw_contract_semantics["functions"].items():

                    inputs_semantics = []
                    for parameter in function["inputs"]:
                        inputs_semantics.append(decode_parameter(parameter))
                    outputs_semantics = []
                    for parameter in function["outputs"]:
                        outputs_semantics.append(decode_parameter(parameter))

                    functions[signature] = FunctionSemantics(
                        signature, function["name"], inputs_semantics, outputs_semantics
                    )

                transformations = dict()
                for signature, parameters_transformations in raw_contract_semantics[
                    "transformations"
                ].items():
                    transformations[signature] = dict()
                    for parameter, transformation in parameters_transformations.items():
                        transformations[signature][parameter] = TransformationSemantics(
                            transformation["transformed_name"],
                            transformation["transformed_type"],
                            transformation["transformation"],
                        )

                contract_semantics = ContractSemantics(
                    raw_contract_semantics["code_hash"],
                    raw_contract_semantics["name"],
                    events,
                    functions,
                    transformations,
                )

            address_semantics = AddressSemantics(
                chain_id,
                address,
                raw_address_semantics["name"],
                raw_address_semantics["is_contract"],
                contract_semantics,
                raw_address_semantics["standard"],
                erc20_semantics,
            )
            return address_semantics

        else:
            return None

    def insert_contract(self, contract, update_if_exist=False):
        contract_with_id = {"_id": contract["code_hash"], **contract}

        if update_if_exist:
            self._contracts.replace_one(
                {"_id": contract_with_id["_id"]}, contract_with_id, upsert=True
            )
        else:
            self._contracts.insert_one(contract_with_id)

    def insert_address(self, address, update_if_exist=False):
        address_with_id = {
            "_id": f"{address['chain_id']}-{address['address']}",
            **address,
        }

        if update_if_exist:
            self._addresses.replace_one(
                {"_id": address_with_id["_id"]}, address_with_id, upsert=True
            )
        else:
            self._addresses.insert_one(address_with_id)

    def insert_signature(self, signature, update_if_exist=False):
        signature_with_id = {"_id": signature["hash"], **signature}

        if update_if_exist:
            self._signatures.replace_one(
                {"_id": signature_with_id["_id"]}, signature_with_id, upsert=True
            )
        else:
            self._signatures.insert_one(signature_with_id)
