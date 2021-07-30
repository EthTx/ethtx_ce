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
import os

import pkg_resources
from flask import current_app, Blueprint
from flask_httpauth import HTTPBasicAuth
from git import Repo

from ethtx_ce.config import Config

bp = Blueprint("deps", __name__)
auth = HTTPBasicAuth()


@bp.before_app_first_request
def read_ethtx_versions() -> None:
    """Read ethtx and ethtx_ce versions."""
    ethtx_version = pkg_resources.get_distribution("ethtx").version

    try:
        ethtx_ce_version = _get_version_from_git()
    except Exception:
        ethtx_ce_version = ""

    current_app.config["ethtx_version"] = ethtx_version
    current_app.config["repo_version"] = ethtx_ce_version


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    """Verify user, return bool."""
    return (
        username == Config.ETHTX_ADMIN_USERNAME
        and password == Config.ETHTX_ADMIN_PASSWORD
    )


def _get_version_from_git() -> str:
    """Get EthTx Ce version from .git"""
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    repo = Repo(root, search_parent_directories=True)

    remote_url = repo.remote("origin").url.replace(".git", "")
    sha = repo.head.object.hexsha

    url = f"{remote_url}/tree/{sha}"

    return url
