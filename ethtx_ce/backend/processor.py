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

from typing import Optional

from flask import Flask

from .processors import ABIProcessor
from .processors import SemanticProcessor
from .providers.semantic_providers.semantics_repository import SemanticsRepository


class EthTxProcessor:
    """ Processor - Abi & Semantics. """

    _abi_processor: ABIProcessor
    _semantic_processor: SemanticProcessor

    def __init__(
        self,
        app: Optional[Flask] = None,
        repository: Optional[SemanticsRepository] = None,
    ):
        self.app = app
        self.repository = repository

        if app and repository:
            self.init_app(app, repository)

    def init_app(self, app: Flask, semantics_repository: SemanticsRepository) -> None:
        """ Init Semantics db in Flask app context. """
        self.app = app
        self._abi_processor = ABIProcessor(repository=semantics_repository)
        self._semantic_processor = SemanticProcessor(repository=semantics_repository)

        app.extensions["abi_processor"]: ABIProcessor = self._abi_processor
        app.extensions[
            "semantics_processor"
        ]: SemanticProcessor = self._semantic_processor

    @property
    def abi_processor(self) -> ABIProcessor:
        """ Abi Processor. """
        return self._abi_processor

    @property
    def semantic_processor(self) -> SemanticProcessor:
        """ Semantic Processor. """
        return self._semantic_processor
