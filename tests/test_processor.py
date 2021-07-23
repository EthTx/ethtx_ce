# from providers.semantics_database.database_connection import MongoConnection
# from providers.SemanticRepository import SemanticRepository
# from models.FullTransaction import FullTransaction
# from processors.abi_processor import ABIProcessor


class TestSemantics:
    pass


# database = MongoConnection()
# semantic_db = SemanticRepository(database)
# semantics = semantic_db.get_event_semantics('mainnet', '0x1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e',
#                                             '0x21281f8d59117d0399dc467dbdd321538ceffe3225e80e2bd4de6f1b3355cbc7')
# assert semantics['name'] == 'LogTransfer'
# semantics = semantic_db.get_function_semantics('mainnet', '0x1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e', '0xa67a6a45')
# assert semantics['name'] == 'operate'
#
# tx = FullTransaction('0x50051e0a6f216ab9484c2080001c7e12d5138250acee1f4b7c725b8fb6bb922d')
# assert tx is not None
#
# processor = ABIProcessor(semantic_db)
# decoded_tx = processor.decode_with_abi(tx)
# assert len(decoded_tx.events) == 39
# assert decoded_tx.events[15].contract_name == 'WETH9'
# assert decoded_tx.events[15].event_name == 'Withdrawal'
# assert len(decoded_tx.calls) == 100
# assert decoded_tx.calls[2].contract_name == 'GasToken2'
# assert decoded_tx.calls[2].function_name == 'balanceOf'
# assert decoded_tx.calls[2].indent == 2
