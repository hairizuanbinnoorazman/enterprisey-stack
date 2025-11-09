import jwt
from jwt import PyJWKClient
import requests

# Important - issuer is very strict
# Every single character needs to be there
# DEX_URL = "http://localhost:9000/application/o/zzz/"
DEX_URL = "http://server:5556"

jwks_url = f"{DEX_URL}/.well-known/openid-configuration"
jwks_uri = requests.get(jwks_url).json()["jwks_uri"]

token = "XXX"
jwks_client = PyJWKClient(jwks_uri)
signing_key = jwks_client.get_signing_key_from_jwt(token)

decoded = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience="XXX", issuer=DEX_URL)
print(decoded)