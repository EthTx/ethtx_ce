import pytest

from app.frontend import create_app


class TestFlask:
    @pytest.fixture
    def client(self):
        ethtx = None
        app = create_app(ethtx)
        with app.test_client() as client:
            yield client

    def test_landing_page(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        # it's a dump check, but it's something
        assert len(resp.data) > 500

    def test_semantics_is_secured_with_basic_auth(self, client):
        tx_hash = "0xf9baa1792d644bbda985324a0bfdc052a806ca1a4b6a3df3578c73025f7fe544"
        url = f"/semantics/mainnet/{tx_hash}/"
        resp = client.get(url)
        assert resp.status_code == 401
