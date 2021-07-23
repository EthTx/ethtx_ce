from datetime import datetime

from ethtx_ce.config import EthConfig
from ethtx_ce.backend.models.objects_model import Event
from tests.mocks.mocks import MockWeb3Provider


class TestDecoders:
    def test_decode_event(self):
        tx = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        receipt = MockWeb3Provider().get_transaction_receipt(tx)
        event = Event(EthConfig.DEFAULT_CHAIN, tx, datetime.now(), receipt.logs[0])
        assert event is not None
