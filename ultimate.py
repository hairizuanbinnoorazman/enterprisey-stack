# import jwt
import requests
from flask import Flask, request, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.oauth2.rfc9068 import JWTBearerTokenValidator
from authlib.oauth2.rfc9068.claims import JWTAccessTokenClaims
from authlib.oauth2 import OAuth2Error
from authlib.jose import jwt, JsonWebKey


app = Flask(__name__)

DEX_URL = "http://127.0.0.1:5556"
DEX_METADATA_URL = f"{DEX_URL}/.well-known/openid-configuration"
JWKS_URL = f"{DEX_URL}/keys"
AUDIENCE = "flask"  # same as in your token

# -------------------------
# 1. Load Dex metadata
# -------------------------
resp = requests.get(DEX_METADATA_URL, timeout=3)
resp.raise_for_status()
dex_metadata = resp.json()

# -------------------------
# 2. Create JWT verifier
# -------------------------
# jwks = requests.get(JWKS_URL).json()
# public_keys = {
#     key["kid"]: jwt.algorithms.RSAAlgorithm.from_jwk(key)
#     for key in jwks["keys"]
# }

# def verify_token(token):
#     headers = jwt.get_unverified_header(token)
#     print(headers)
#     key = public_keys[headers["kid"]]
#     return jwt.decode(token, key=key, audience=AUDIENCE, algorithms=["RS256"])

# -------------------------
# 3. ResourceProtector setup (optional for later token validation)
# -------------------------
require_oauth = ResourceProtector()

class MyJWTBearerTokenValidator(JWTBearerTokenValidator):
    def get_jwks(self):
        resp = requests.get(f"{DEX_URL}/.well-known/openid-configuration").json()
        resp2 = requests.get(resp["jwks_uri"]).json()
        return JsonWebKey.import_key_set(resp2)
    
    def authenticate_token(self, token_string):
        """"""
        # empty docstring avoids to display the irrelevant parent docstring

        claims_options = {
            "iss": {"essential": True, "validate": self.validate_iss},
            "exp": {"essential": True},
            "aud": {"essential": True, "value": self.resource_server},
            "sub": {"essential": True},
            "client_id": {"essential": False},
            "iat": {"essential": True},
            "jti": {"essential": False},
            "auth_time": {"essential": False},
            "acr": {"essential": False},
            "amr": {"essential": False},
            "scope": {"essential": False},
            "groups": {"essential": False},
            "roles": {"essential": False},
            "entitlements": {"essential": False},
        }
        jwks = self.get_jwks()

        # If the JWT access token is encrypted, decrypt it using the keys and algorithms
        # that the resource server specified during registration. If encryption was
        # negotiated with the authorization server at registration time and the incoming
        # JWT access token is not encrypted, the resource server SHOULD reject it.

        # The resource server MUST validate the signature of all incoming JWT access
        # tokens according to [RFC7515] using the algorithm specified in the JWT 'alg'
        # Header Parameter. The resource server MUST reject any JWT in which the value
        # of 'alg' is 'none'. The resource server MUST use the keys provided by the
        # authorization server.
        try:
            return jwt.decode(
                token_string,
                key=jwks,
                claims_cls=JWTAccessTokenClaims,
                claims_options=claims_options,
            )
        except DecodeError as exc:
            raise InvalidTokenError(
                realm=self.realm, extra_attributes=self.extra_attributes
            ) from exc


require_oauth.register_token_validator(MyJWTBearerTokenValidator(issuer=DEX_URL, resource_server="flask"))

# @app.before_request
# def check_auth():
#     if request.path == "/health":
#         return
#     auth = request.headers.get("Authorization", "")
#     if not auth.startswith("Bearer "):
#         return jsonify({"error": "Missing bearer token"}), 401
#     token = auth.split()[1]
#     try:
#         claims = verify_token(token)
#         request.user = claims
#     except Exception as e:
#         return jsonify({"error": str(e)}), 401

@app.route("/.well-known/oauth-authorization-server")
def oauth_metadata():
    """
    Tell clients that this API (App B) uses Dex as its Authorization Server.
    """
    return jsonify({
        "issuer": DEX_URL,
        "authorization_endpoint": dex_metadata["authorization_endpoint"],
        "token_endpoint": dex_metadata["token_endpoint"],
        "userinfo_endpoint": dex_metadata.get("userinfo_endpoint"),
        "jwks_uri": dex_metadata["jwks_uri"],
        "scopes_supported": dex_metadata.get("scopes_supported", []),
        "response_types_supported": dex_metadata.get("response_types_supported", []),
        "grant_types_supported": dex_metadata.get("grant_types_supported", []),
        "code_challenge_methods_supported": dex_metadata.get("code_challenge_methods_supported", []),
    })


@app.route("/api/resource")
@require_oauth()
def resource():
    token = current_token  # guaranteed to exist here because decorator already validated
    user_email = token.email
    return jsonify({"message": f"Hello {user_email}!"})

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)