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

from .mongo_db import MongoDb
from .providers.semantic_providers.semantics_database import SemanticsDatabase
from .providers.semantic_providers.semantics_repository import SemanticsRepository


class SemanticsDb:
    """ Semantics Database. """

    _semantics_db: SemanticsDatabase = None
    _semantics_repository: SemanticsRepository = None

    def __init__(
        self, app: Optional[Flask] = None, db_engine: Optional[MongoDb] = None
    ):
        self.app = app
        self._db = db_engine.db if db_engine else db_engine

        if db_engine and app:
            self.init_app(app, db_engine)

    def init_app(self, app: Flask, db: MongoDb) -> None:
        """ Init Semantics db in Flask app context. """
        self.app = app
        self._semantics_db = SemanticsDatabase(db.db)
        self._semantics_repository = SemanticsRepository(self._semantics_db)

        app.extensions["semantics_db"]: SemanticsDatabase = self._semantics_db
        app.extensions[
            "semantics_repository"
        ]: SemanticsRepository = self._semantics_repository

    @property
    def repository(self) -> SemanticsRepository:
        """ Semantics repository. """
        return self._semantics_repository

    @property
    def db(self) -> SemanticsDatabase:
        """ Semantics database. """
        return self._semantics_db
