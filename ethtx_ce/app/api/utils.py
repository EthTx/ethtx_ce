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

from dataclasses import asdict
from functools import wraps
from typing import Dict
from decimal import Decimal


def enable_direct(decorator):
    """Decorator direct helper."""

    @wraps(decorator)
    def wrapper(*args, **kwargs):
        f = args[0]
        if callable(f):
            return decorator()(f)  # pass the function to be decorated
        else:
            return decorator(*args, **kwargs)  # pass the specified params

    return wrapper


def as_dict(cls):
    """Return object as dict."""

    def wrapper(*args, **kwargs) -> Dict:
        instance = cls(*args, **kwargs)
        return asdict(instance)

    return wrapper


def delete_bstrings(obj):
    primitive = (int, str, bool, float, Decimal, type(None))

    if isinstance(obj, primitive):
        return obj
    elif type(obj) == bytes:
        return obj.decode()
    elif type(obj) == list:
        for index, value in enumerate(obj):
            obj[index] = delete_bstrings(value)
    elif type(obj) == dict:
        for index, value in obj.items():
            obj[index] = delete_bstrings(value)
    else:
        raise Exception("Unknown type:" + str(type(obj)))

    return obj
