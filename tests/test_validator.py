import pytest

from ethtx_ce.backend.models.objects_model import Transaction
from ethtx_ce.backend.validators import assert_tx_hash_is_correct


class TestValidator:
    def test_transaciton_invalid_hash_gets_exception(self):
        invalid_hashes = ["", "test", "Haxl337", None, 1]

        for invalid_hash in invalid_hashes:
            with pytest.raises(Exception):
                Transaction(invalid_hash)

    def test_tx_valid_hash(self):
        tx_hash = "0xe9a781eea6b6dbb9354555fff3cfb4727d27eea78346f2ca341e3268037eb559"
        assert_tx_hash_is_correct(tx_hash)
