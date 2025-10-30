import jwt
from jwt import PyJWKClient
import requests

DEX_URL = "http://127.0.0.1:5556"

jwks_url = f"{DEX_URL}/.well-known/openid-configuration"
jwks_uri = requests.get(jwks_url).json()["jwks_uri"]

token = "xxx"
jwks_client = PyJWKClient(jwks_uri)
signing_key = jwks_client.get_signing_key_from_jwt(token)

decoded = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience="flask", issuer=DEX_URL)
print(decoded)