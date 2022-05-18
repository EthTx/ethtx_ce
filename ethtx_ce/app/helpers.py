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
import os
import pkgutil
from typing import Any, List, Tuple, Optional

import pkg_resources
import requests
from flask import Blueprint, Flask
from git import Repo

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


def class_import(name: str) -> Any:
    """Import class from string."""
    d = name.rfind(".")
    classname = name[d + 1 : len(name)]
    m = __import__(name[0:d], globals(), locals(), [classname])

    return getattr(m, classname)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def read_ethtx_versions(app: Flask) -> None:
    """Read ethtx and ethtx_ce versions."""
    ethtx_version = pkg_resources.get_distribution("ethtx").version

    try:
        remote_url, sha = _get_version_from_git()
    except Exception:
        remote_url, sha = _get_version_from_docker()

    ethtx_ce_version = f"{_clean_up_git_link(remote_url)}/tree/{sha}"

    log.info(
        "%s: EthTx version: %s. EthTx CE version: %s",
        app.name,
        ethtx_version,
        ethtx_ce_version,
    )

    app.config["ethtx_version"] = ethtx_version
    app.config["ethtx_ce_version"] = ethtx_ce_version


def get_latest_ethtx_version() -> str:
    """Get latest EthTx version."""
    package = "EthTx"
    response = requests.get(f"https://pypi.org/pypi/{package}/json")

    if response.status_code != 200:
        log.warning("Failed to get latest EthTx version from PyPI")
        return ""

    log.info("Latest EthTx version: %s", response.json()["info"]["version"])
    return response.json()["info"]["version"]


def _get_version_from_git() -> Tuple[str, str]:
    """Get EthTx CE version from .git"""
    repo = Repo(__file__, search_parent_directories=True)

    remote_url = repo.remote("origin").url
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=True)

    return remote_url, short_sha


def _get_version_from_docker() -> Tuple[str, str]:
    """Get EthTx CE version from env."""
    return os.getenv("GIT_URL", ""), os.getenv("GIT_SHA", "")


def _clean_up_git_link(git_link: str) -> str:
    """Clean up git link, delete .git extension, make https url."""
    if "@" in git_link:
        git_link.replace(":", "/").replace("git@", "https://")

    if git_link.endswith(".git"):
        git_link = git_link[:-4]

    return git_link
