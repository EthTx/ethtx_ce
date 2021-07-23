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
from pymongo import MongoClient, database


class MongoDb:
    """ Mongo Database. """

    _db = None
    _client = None

    def __init__(self, app: Optional[Flask] = None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """ Init Semantic db in Flask app context. """
        self.app = app
        self._init_client()
        self._db = self._client[self.app.config["MONGODB_DB"]]

        app.extensions["db"]: database.Database = self._db
        app.extensions["db_client"]: MongoClient = self._client

    def _init_client(self) -> None:
        """ Init db client. """

        if self.app.config["ENV"] == "development":
            self._client = MongoClient(
                "mongodb://%s/%s"
                % (self.app.config["MONGODB_HOST"], self.app.config["MONGODB_DB"])
            )
        else:
            self._client = MongoClient(
                "mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority"
                % (
                    self.app.config["MONGODB_USERNAME"],
                    self.app.config["MONGODB_PASSWORD"],
                    self.app.config["MONGODB_HOST"],
                    self.app.config["MONGODB_DB"],
                )
            )

    @property
    def client(self) -> MongoClient:
        """ Db Client. """
        return self._client

    @property
    def db(self) -> database.Database:
        """" Db. """
        return self._db
