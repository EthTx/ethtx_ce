# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

from flask import render_template, Blueprint, current_app

from . import frontend_route

bp = Blueprint("static", __name__)


@frontend_route(bp, "/")
def search_page() -> render_template:
    """Render search page - index."""
    return (
        render_template(
            "index.html",
            chains=current_app.ethtx.providers.web3provider.nodes.keys()
            if current_app.ethtx
            else [],
            ethtx_version=current_app.config["ethtx_version"],
            ethtx_ce_version=current_app.config["ethtx_ce_version"],
        ),
        200,
    )
