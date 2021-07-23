import pytest

from ethtx_ce.backend.exceptions import Web3ConnectionException
from ethtx_ce.backend.providers.web3_provider import Web3Provider, connect_chain


class TestW3RepositoryForMainnet:
    """
    WARNING!
    Those are connection tests, they test connection to eth node and accessibility to different functions.
    If those fail, make sure you configuration for you node is ok, and that node is up.
    """

    def test_invalid_chain_id(self):
        Web3Provider._instances = {}
        with pytest.raises(AssertionError):
            Web3Provider("deadbeef")

    def test_failed_connection(self):
        with pytest.raises(Web3ConnectionException) as e:
            connect_chain("not_a_valid_url")

    def test_get_block(self):
        w3 = Web3Provider("mainnet")
        block = w3.get_block(13242)

        assert block is not None
        assert block.difficulty == 794805539069
        assert block.gas_limit == 5000
        assert block.gas_used == 0
        assert (
            block.hash
            == b"F?f\xbf\xc5\x06\xafq_\xa8a%\xa2\xa7\xa7\xa4\x95N\xa5\n2O#\x96\x90\x86t\xb7\xb8\xbe\xc5\x9b"
        )
        assert block.miner == "0xBbeD46565f5aA9aF9539f543067821fA4B565438"
        assert block.nonce == b"\xa7\x1c\x11d\x7fc\xaad"
        assert block.number == 13242
        assert (
            block.parentHash
            == b"9\x8cz$I\xa8\x94\xf7KEw\xe9\x11L\x1d\xb7\x8eG\xebd>2\r:8t\xaa\t<#\xb8\xc5"
        )
        assert (
            block.receiptsRoot
            == b"V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n[H\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!"
        )
        assert (
            block.sha3Uncles
            == b"\x1d\xccM\xe8\xde\xc7]z\xab\x85\xb5g\xb6\xcc\xd4\x1a\xd3\x12E\x1b\x94\x8at\x13\xf0\xa1B\xfd@\xd4\x93G"
        )
        assert block.size == 546
        assert (
            block.stateRoot
            == b"\x13\x82c\xb5'/iU\xcb\x8a\x8c9\xd6e\xf7\x18\\5\x12\xae\xf1\x04\xfe\x993K\x884%Uy;"
        )
        assert block.timestamp == 1438379420
        assert block.totalDifficulty == 4547128234564645
        assert block.transactions == []
        assert (
            block.transactionsRoot
            == b"V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n[H\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!"
        )
        assert block.uncles == []

    def test_get_transaction(self):
        w3 = Web3Provider("mainnet")
        tx = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        tx = w3.get_transaction(tx)

        assert tx is not None
        assert (
            tx.blockHash
            == b"\xafl&\xdb&0\xa2\xd7E\xad|\x83\x1e \x15r\x1e3{\xc4T\xaa\x83\x15\xc7\xb6\xfb\xb8tNF8"
        )
        assert tx.blockNumber == 11958607
        assert tx.from_address == "0x077ef243AD02c739cA7951CF68e70d24c0CEcAFa"
        assert tx.gas == 168135
        assert (
            tx.hash
            == b"\xd7p\x1a\x0f\xc0U\x93\xae\xe3\xa1o \xca\xb6\x05\xdbq\x83\xf7R\xae\x94,\xc7_\xd0\x97_\xea\xf1\x07."
        )
        assert tx.nonce == 13
        assert (
            tx.r
            == b"<t\x81\xecL\xc1\xb8\x1b\xed&inz\xfa \xa1\xd2\xac\xf9v\xb7\x12\x155!)\xd4\x7f^t#\xe8"
        )
        assert (
            tx.s
            == b"j\xec8\x02D\xe8\xbf\xc6\xfe\x19'\xc1\n\xc6#:\r\xe7\xc9J\x8c\xcc\xb9m\x8cS\x80\x1f\x04?ug"
        )
        assert tx.to_address == "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
        assert tx.transactionIndex == 135
        assert tx.v == 38
        assert tx.value == 0

    def test_get_code_hash(self):
        contract_address = "0x51ea5526e47b7b7668f3088906acbd3552970fdb"
        w3 = Web3Provider("mainnet")
        code_hash = w3.get_code_hash(contract_address)
        assert (
            code_hash
            == "0x2e3e6bc45aed2f69b7cb5d957f303583c04c4ab4a394cea55a5c70eecae3087c"
        )

    def test_guess_token(self):
        w3 = Web3Provider("mainnet")

        akita_contract_address = "0x51ea5526e47b7b7668f3088906acbd3552970fdb"
        akita_token = w3.guess_erc20_token(akita_contract_address)

        assert akita_token is not None
        assert akita_token == {
            "address": "0x51ea5526e47b7b7668f3088906acbd3552970fdb",
            "symbol": "AKITASWAP",
            "name": "AKITASWAP",
            "decimals": 18,
        }

        random_contract_address = "0x19c0976f590D67707E62397C87829d896Dc0f1F1"
        token = w3.guess_erc20_token(random_contract_address)

        assert token is None

    def test_get_call_tree(self):
        w3 = Web3Provider("mainnet")
        tx = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        call_tree = w3.get_calls(tx)

        assert call_tree is not None
        assert len(call_tree.calls) == 5
        assert call_tree.error == None
        assert call_tree.from_address == "0x077ef243ad02c739ca7951cf68e70d24c0cecafa"
        assert call_tree.gas == "0x2368f"
        assert call_tree.gasUsed == "0x1f380"
        assert call_tree.to_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call_tree.type == "CALL"
        assert call_tree.value == "0x0"

        call0 = call_tree.calls[0]
        assert call0.calls == []
        assert call0.error is None
        assert call0.from_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call0.gas == "0x2200e"
        assert call0.gasUsed == "0x4b4"
        assert call0.time is None  # TODO: should it be none?
        assert call0.to_address == "0x5201883feeb05822ce25c9af8ab41fc78ca73fa9"
        assert call0.type == "STATICCALL"
        assert call0.value is None

        call1 = call_tree.calls[1]
        assert call1.calls == []
        assert call1.error is None
        assert call1.from_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call1.gas == "0x20e53"
        assert call1.gasUsed == "0x58a0"
        assert call1.time is None  # TODO: should it be none?
        assert call1.to_address == "0x8290333cef9e6d528dd5618fb97a76f268f3edd4"
        assert call1.type == "CALL"
        assert call1.value == "0x0"

        call2 = call_tree.calls[2]
        assert len(call2.calls) == 3
        assert call2.error is None
        assert call2.from_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call2.gas == "0x1a9e7"
        assert call2.gasUsed == "0x11834"
        assert call2.time is None  # TODO: should it be none?
        assert call2.to_address == "0x5201883feeb05822ce25c9af8ab41fc78ca73fa9"
        assert call2.type == "CALL"
        assert call2.value == "0x0"

        call3 = call_tree.calls[3]
        assert len(call3.calls) == 1
        assert call3.error is None
        assert call3.from_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call3.gas == "0x8f7b"
        assert call3.gasUsed == "0x2e93"
        assert call3.time is None  # TODO: should it be none?
        assert call3.to_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        assert call3.type == "CALL"
        assert call3.value == "0x0"

        call3_1 = call3.calls[0]
        assert len(call3_1.calls) == 0
        assert call3_1.error is None
        assert call3_1.from_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        assert call3_1.gas == "0x8fc"
        assert call3_1.gasUsed == "0x53"
        assert call3_1.time is None  # TODO: should it be none?
        assert call3_1.to_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call3_1.type == "CALL"
        assert call3_1.value == "0x10f5cf5a2cb32048"

        call4 = call_tree.calls[4]
        assert len(call4.calls) == 0
        assert call4.error is None
        assert call4.from_address == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        assert call4.gas is None
        assert call4.gasUsed is None
        assert call4.input == "0x"
        assert call4.output == "0x"
        assert call4.time is None  # TODO: should it be none?
        assert call4.to_address == "0x077ef243ad02c739ca7951cf68e70d24c0cecafa"
        assert call4.type == "CALL"
        assert call4.value == "0x10f5cf5a2cb32048"

    def test_get_tx_receipt(self):
        w3 = Web3Provider("mainnet")
        tx = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        receipt = w3.get_transaction_receipt(tx)

        assert receipt is not None
        assert (
            receipt.blockHash
            == b"\xafl&\xdb&0\xa2\xd7E\xad|\x83\x1e \x15r\x1e3{\xc4T\xaa\x83\x15\xc7\xb6\xfb\xb8tNF8"
        )
        assert receipt.blockNumber == 11958607
        assert receipt.contractAddress is None
        assert receipt.cumulativeGasUsed == 12418533
        assert receipt.from_address == "0x077ef243AD02c739cA7951CF68e70d24c0CEcAFa"
        assert receipt.gasUsed == 112568
        assert len(receipt.logs) == 5
        assert receipt.root is None
        assert receipt.status == 1
        assert receipt.to_address == "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
        assert (
            receipt.transactionHash
            == b"\xd7p\x1a\x0f\xc0U\x93\xae\xe3\xa1o \xca\xb6\x05\xdbq\x83\xf7R\xae\x94,\xc7_\xd0\x97_\xea\xf1\x07."
        )
        assert receipt.transactionIndex == 135

        log0 = receipt.logs[0]

        assert log0.address == "0x8290333ceF9e6D528dD5618Fb97a76f268f3EDD4"
        assert (
            log0.blockHash
            == b"\xafl&\xdb&0\xa2\xd7E\xad|\x83\x1e \x15r\x1e3{\xc4T\xaa\x83\x15\xc7\xb6\xfb\xb8tNF8"
        )
        assert log0.blockNumber == 11958607
        assert (
            log0.data
            == "0x000000000000000000000000000000000000000000000e54e035c8e8b9ac4ef6"
        )
        assert log0.logIndex == 373
        assert log0.removed == False

        assert (
            log0.topics[0]
            == b"\xdd\xf2R\xad\x1b\xe2\xc8\x9bi\xc2\xb0h\xfc7\x8d\xaa\x95+\xa7\xf1c\xc4\xa1\x16(\xf5ZM\xf5#\xb3\xef"
        )
        assert (
            log0.topics[1]
            == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07~\xf2C\xad\x02\xc79\xcayQ\xcfh\xe7\r$\xc0\xce\xca\xfa"
        )
        assert (
            log0.topics[2]
            == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00R\x01\x88?\xee\xb0X"\xce%\xc9\xaf\x8a\xb4\x1f\xc7\x8c\xa7?\xa9'
        )

        assert (
            log0.transactionHash
            == b"\xd7p\x1a\x0f\xc0U\x93\xae\xe3\xa1o \xca\xb6\x05\xdbq\x83\xf7R\xae\x94,\xc7_\xd0\x97_\xea\xf1\x07."
        )

        assert log0.transactionIndex == 135

        log1 = receipt.logs[1]

        assert log1.address == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        assert (
            log1.blockHash
            == b"\xafl&\xdb&0\xa2\xd7E\xad|\x83\x1e \x15r\x1e3{\xc4T\xaa\x83\x15\xc7\xb6\xfb\xb8tNF8"
        )
        assert log1.blockNumber == 11958607
        assert (
            log1.data
            == "0x00000000000000000000000000000000000000000000000010f5cf5a2cb32048"
        )
        assert log1.logIndex == 374
        assert log1.removed == False

        assert (
            log1.topics[0]
            == b"\xdd\xf2R\xad\x1b\xe2\xc8\x9bi\xc2\xb0h\xfc7\x8d\xaa\x95+\xa7\xf1c\xc4\xa1\x16(\xf5ZM\xf5#\xb3\xef"
        )
        assert (
            log1.topics[1]
            == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00R\x01\x88?\xee\xb0X"\xce%\xc9\xaf\x8a\xb4\x1f\xc7\x8c\xa7?\xa9'
        )
        assert (
            log1.topics[2]
            == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00z%\rV0\xb4\xcfS\x979\xdf,]\xac\xb4\xc6Y\xf2H\x8d"
        )

        assert (
            log1.transactionHash
            == b"\xd7p\x1a\x0f\xc0U\x93\xae\xe3\xa1o \xca\xb6\x05\xdbq\x83\xf7R\xae\x94,\xc7_\xd0\x97_\xea\xf1\x07."
        )
        assert log1.transactionIndex == 135

        log4 = receipt.logs[4]
        assert log4.address == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        assert (
            log4.blockHash
            == b"\xafl&\xdb&0\xa2\xd7E\xad|\x83\x1e \x15r\x1e3{\xc4T\xaa\x83\x15\xc7\xb6\xfb\xb8tNF8"
        )
        assert log4.blockNumber == 11958607
        assert (
            log4.data
            == "0x00000000000000000000000000000000000000000000000010f5cf5a2cb32048"
        )
        assert log4.logIndex == 377
        assert log4.removed == False
        assert (
            log4.topics[0]
            == b"\x7f\xcfS,\x15\xf0\xa6\xdb\x0b\xd6\xd0\xe08\xbe\xa7\x1d0\xd8\x08\xc7\xd9\x8c\xb3\xbfrh\xa9[\xf5\x08\x1be"
        )
        assert (
            log4.topics[1]
            == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00z%\rV0\xb4\xcfS\x979\xdf,]\xac\xb4\xc6Y\xf2H\x8d"
        )
        assert (
            log4.transactionHash
            == b"\xd7p\x1a\x0f\xc0U\x93\xae\xe3\xa1o \xca\xb6\x05\xdbq\x83\xf7R\xae\x94,\xc7_\xd0\x97_\xea\xf1\x07."
        )
        assert log4.transactionIndex == 135
