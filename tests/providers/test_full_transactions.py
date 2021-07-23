from ethtx_ce.backend.models.objects_model import FullTransaction


class TestFullTxes:
    def test_create_full_transactions(self):

        tx_hashes = [
            "0x50051e0a6f216ab9484c2080001c7e12d5138250acee1f4b7c725b8fb6bb922d",
            "0x276ed3eda11815e23148bb4e3c886b7a0e383293437e32f40ba1b055ddf9b2ec",
        ]

        for tx_hash in tx_hashes:
            FullTransaction(tx_hash)
