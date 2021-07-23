from ethtx_ce.backend.models.objects_model import FullTransaction
from ethtx_ce.backend.processors import ABIProcessor
from ethtx_ce.backend.processors import SemanticProcessor
from ethtx_ce.backend.providers.semantic_providers.semantics_database import (
    SemanticsDatabase,
)
from ethtx_ce.backend.providers.semantic_providers.semantics_repository import (
    SemanticsRepository,
)


class TestEndToEnd:
    def test_decoded(self):
        database = SemanticsDatabase()
        semantic_db = SemanticsRepository(database)
        semantics = semantic_db.get_event_abi(
            "mainnet",
            "0x1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e",
            "0x21281f8d59117d0399dc467dbdd321538ceffe3225e80e2bd4de6f1b3355cbc7",
        )
        assert semantics.name == "LogTransfer"
        semantics = semantic_db.get_function_abi(
            "mainnet", "0x1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e", "0xa67a6a45"
        )
        assert semantics.name == "operate"

        tx = FullTransaction(
            "0x50051e0a6f216ab9484c2080001c7e12d5138250acee1f4b7c725b8fb6bb922d"
        )
        assert tx is not None

        processor = ABIProcessor(semantic_db)
        decoded_tx = processor.decode_with_abi(tx)
        assert len(decoded_tx.events) == 39
        assert decoded_tx.events[15].contract_name == "WETH9"
        assert decoded_tx.events[15].event_name == "Withdrawal"
        assert len(decoded_tx.calls) == 100
        assert decoded_tx.calls[2].to_name == "GasToken2"
        assert decoded_tx.calls[2].function_name == "balanceOf"
        assert decoded_tx.calls[2].indent == 2
        assert len(decoded_tx.transfers) == 17
        assert decoded_tx.transfers[5].token_symbol == "DAI"
        assert decoded_tx.transfers[5].value == 36828.0
        assert len(decoded_tx.balances) == 9

        processor = SemanticProcessor(semantic_db)
        decoded_tx = processor.decode_with_semantics(decoded_tx)
        assert len(decoded_tx.events) == 39
        assert decoded_tx.events[0].contract.name == "DSProxy"
        assert decoded_tx.events[0].contract.badge == "receiver"
        assert decoded_tx.events[0].event_name == "LogNote"
        assert len(decoded_tx.calls) == 100
        assert decoded_tx.calls[0].to_address.name == "DSProxy"
        assert decoded_tx.calls[0].to_address.badge == "receiver"
        assert decoded_tx.calls[0].function_name == "execute"
        assert decoded_tx.calls[6].call_type == "delegatecall"
        assert decoded_tx.calls[6].arguments[1].value["name"] == "MCD_DAI"
