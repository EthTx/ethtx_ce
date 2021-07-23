from datetime import datetime

from ethtx_ce.config import EthConfig
from ethtx_ce.backend.models.objects_model import Block, Event, Transaction
from mocks.mocks import MockWeb3Provider


class TestModel:
    def test_create_transaction(self):
        tx_hash = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        mock_web3_provider = MockWeb3Provider()
        tx = Transaction(tx_hash, web3provider=mock_web3_provider)
        assert tx is not None
        self._check_some_attributes_of_tx(tx)

    def test_create_block(self):
        mock_web3_provider = MockWeb3Provider()
        block = Block(1, web3provider=mock_web3_provider)
        # block = Block(1)
        assert block is not None
        self._check_some_attributes_of_block(block)

    def _check_some_attributes_of_block(self, block: Block):
        assert block is not None
        assert block.block_number is not None
        assert block.block_hash is not None
        assert block.timestamp is not None
        assert block.miner is not None
        assert block.tx_count is not None

    def _check_some_attributes_of_tx(self, tx: Transaction):
        assert tx.tx_hash is not None
        assert tx.from_address is not None
        assert tx.to_address is not None
        assert tx.timestamp is not None
        assert tx.tx_index is not None

    def test_create_event_from_tx_hash(self):
        tx = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        receipt = MockWeb3Provider().get_transaction_receipt(tx)
        e = Event(EthConfig.DEFAULT_CHAIN, tx, datetime.now(), receipt.logs[0])

        assert e is not None
        assert e.chain_id is not None
        assert e.tx_hash is not None
        assert e.timestamp is not None
        assert e.log_index is not None
