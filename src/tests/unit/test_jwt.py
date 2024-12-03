from app.containers import Container


class TestAuth:
    async def test_encode_decode_rsa(self, container: Container):
        payload = {"some_key": "some_value"}

        access_token = await container.user.jwt_rsa_service().encode(payload, "access")

        decoded_payload = await container.user.jwt_rsa_service().decode(access_token)

        assert payload["some_key"] == decoded_payload["some_key"]

    async def test_encode_decode_hmac(self, container: Container):
        payload = {"some_key": "some_value"}

        access_token = await container.user.jwt_hmac_service().encode(payload, "access")

        decoded_payload = await container.user.jwt_hmac_service().decode(access_token)

        assert payload["some_key"] == decoded_payload["some_key"]
