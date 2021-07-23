import pytest

from ethtx_ce.backend.exceptions import InvalidTransactionHash
from ethtx_ce.backend.models.objects_model import Transaction, Call


class TestExceptions:
    def test_tx_with_invalid_hash(self):

        with pytest.raises(InvalidTransactionHash):
            Call("invalid")

        with pytest.raises(InvalidTransactionHash):
            Transaction("asnc")
