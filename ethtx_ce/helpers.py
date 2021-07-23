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

import importlib
import logging
import pkgutil
import sys
import time
from typing import Any, List, Union, Callable, Tuple, Set

from flask import Blueprint, Flask

log = logging.getLogger(__name__)


def register_blueprints(
    app: Flask, package_name: str, package_path: str
) -> List[Blueprint]:
    """
    Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.
    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []

    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)

    return rv


def register_extensions(
    extensions: List[Union[Callable, Tuple[Callable, Set[str]]]], flask_app: Flask
) -> None:
    """
    Register extensions in app.
    It allows to register some extensions before registering blueprints.
    Also if some extensions are related, it can deals with that.

    :param extensions:  - Single callable object with init_app method
                        - Tuple of Callable object and Set of app_extensions.

    For example:
        extensions=[mongo_db, (semantics_db, {"db"}),
            eth_tx_processor, {"semantics_repository"})])
        - mongo_db object needs only Flask
        - semantics_db during init_app requires Flask and db kwarg,
         so we have to register mongo in Flask app extensions:
            app[db] = mongo_db
            After that, we have mongo_db in app context, so semantics_db can access to it.
            Also semantics registered in app context - semantics_repository.
        - etx_tx_processor - like above, object needs Flask and `semantics_repository` kwarg. We got in app extensions
            `semantics_repository` so we can get it and pass to `semantics_repository` kwarg.

    """
    for extension in extensions:
        if not isinstance(extension, tuple):
            extension.init_app(app=flask_app)
        else:
            app_extensions = {ext: flask_app.extensions[ext] for ext in extension[1]}
            extension[0].init_app(app=flask_app, **app_extensions)


def class_import(name: str) -> Any:
    """ Import class from string. """
    d = name.rfind(".")
    classname = name[d + 1 : len(name)]
    m = __import__(name[0:d], globals(), locals(), [classname])

    return getattr(m, classname)


class RecursionLimit:
    """ Increase maximum recursion depth. """

    def __init__(self, limit: int):
        self.limit = limit
        self.cur_limit = sys.getrecursionlimit()

    def __enter__(self) -> None:
        sys.setrecursionlimit(self.limit)

    def __exit__(self, *_) -> None:
        sys.setrecursionlimit(self.cur_limit)


class Singleton(type):
    """ Singleton - restricts the instantiation of a class to one object. """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ExecutionTimer:
    """ Execution Timer Context. """

    start_time: float
    part_name: str

    def __init__(self, part_name: str):
        self.part_name = part_name

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, *kwargs):
        end_time = time.time()
        exec_time = (end_time - self.start_time) * 1000
        log.info("Executed %s in %s ms", self.part_name, exec_time)


class AttrDict(dict):
    """ AttrDict class. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
