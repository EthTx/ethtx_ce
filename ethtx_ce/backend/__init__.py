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

from flask import Flask

from ethtx_ce import factory
from .processor import EthTxProcessor
from .mongo_db import MongoDb
from .semantic_db import SemanticsDb

mongo_db = MongoDb()
semantics_db = SemanticsDb()
eth_tx_processor = EthTxProcessor()


def create_app(settings_override: Optional[Dict] = None) -> Flask:
    """Returns the backend application instance. """
    app = factory.create_app(
        __name__,
        __path__,
        settings_override,
        extensions=[
            mongo_db,
            (semantics_db, {"db"}),
            (eth_tx_processor, {"semantics_repository"}),
        ],
    )

    return app
