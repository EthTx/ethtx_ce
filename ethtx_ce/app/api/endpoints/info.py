from flask import Blueprint, current_app

from .. import api_route
from ..decorators import response
from ...helpers import get_latest_ethtx_version

info_bp = Blueprint("api_info", __name__)


@api_route(info_bp, "/info")
@response(200)
def read_info():
    """Get info."""
    ethtx_version = current_app.config["ethtx_version"]
    latest_ethtx_version = get_latest_ethtx_version()

    ethtx_ce_version = current_app.config["ethtx_ce_version"]

    return {
        "ethtx": {
            "version": ethtx_version,
            "is_latest": ethtx_version == latest_ethtx_version,
        },
        "ethtx_ce": {
            "version": ethtx_ce_version,
        },
    }
