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
import os
from typing import Tuple, Optional

import pkg_resources
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from git import Repo

from ethtx_ce.config import Config

log = logging.getLogger(__name__)

auth = HTTPBasicAuth()


def read_ethtx_versions(app: Flask) -> None:
    """Read ethtx and ethtx_ce versions."""
    ethtx_version = pkg_resources.get_distribution("ethtx").version

    try:
        remote_url, sha = _get_version_from_git()
    except Exception:
        remote_url, sha = _get_version_from_docker()
    ethtx_ce_version = f"{remote_url}/tree/{sha}"

    log.info("EthTx version: %s. EthTx CE version: %s", ethtx_version, ethtx_ce_version)

    app.config["ethtx_version"] = ethtx_version
    app.config["repo_version"] = ethtx_ce_version


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    """Verify user, return bool."""
    return (
        username == Config.ETHTX_ADMIN_USERNAME
        and password == Config.ETHTX_ADMIN_PASSWORD
    )


def _get_version_from_git() -> Tuple[str, str]:
    """Get EthTx CE version from .git"""
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    repo = Repo(root)

    remote_url = repo.remote("origin").url.replace(".git", "")
    sha = repo.head.object.hexsha

    return remote_url, sha


def _get_version_from_docker(
    path: Optional[str] = "/app/git_version"
) -> Tuple[str, str]:
    """Get EthTx CE version from file."""
    if path and os.path.isfile(path):
        with open(path) as f:
            url_sha = f.readline().strip().split(",")
    else:
        url_sha = ["", ""]

    if url_sha:
        return url_sha[0], url_sha[1]
