import os
import json
import time
import base64
from flask import Flask, request, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.oauth2 import OAuth2Error
from authlib.jose import jwt, JsonWebToken, JsonWebKey
from authlib.jose.errors import ExpiredTokenError, JoseError
import requests

app = Flask(__name__)

DEX_URL = os.environ['OIDC_ISSUER']
DEX_METADATA_URL = f"{DEX_URL}.well-known/openid-configuration"
JWKS_URL = requests.get(DEX_METADATA_URL).json()["jwks_uri"]
AUDIENCE = os.environ['OIDC_CLIENT_ID']

resp = requests.get(DEX_METADATA_URL, timeout=3)
resp.raise_for_status()
dex_metadata = resp.json()

require_oauth = ResourceProtector()

class SimpleRemoteJWTValidator:
    """Validate JWTs using JWKS from the authorization server, no caching."""

    TOKEN_TYPE = "bearer" 
    realm = "api" 

    def __init__(self, jwks_url, audience=None, algs=None):
        super().__init__()
        self.jwks_url = jwks_url
        self.audience = audience
        self.algs = algs or ["RS256"]
        self.jwt = JsonWebToken(self.algs)

    def get_jwks(self):
        resp = requests.get(self.jwks_url)
        resp.raise_for_status()
        jwks = resp.json()
        return jwks

    def authenticate_token(self, token_string):
        keys = self.get_jwks()
        key = JsonWebKey.import_key_set(keys)

        # Decode and verify signature
        claims = self.jwt.decode(token_string, key)
        claims.validate_exp(int(time.time()), 30)

        if self.audience and claims.get("aud") != self.audience:
            raise ValueError("Invalid audience")

        return claims
    
    def validate_token(self, claims, scopes, req, **kwargs):
        request.user = claims
        return request
        
    def validate_request(self, request):
        """Required by ResourceProtector — extracts and validates token."""
        auth_header = request.headers.get("Authorization")
        print(auth_header)
        token_string = auth_header.split(" ", 1)[1].strip()
        if not token_string:
            raise ValueError("Missing access token")

        token = self.authenticate_token(token_string)
        request.token = token
        return token

    def request_invalid(self, request):
        """Optional: check malformed requests."""
        return False

    def token_revoked(self, token):
        """Optional: check token revocation (not implemented)."""
        return False
    
require_oauth.register_token_validator(SimpleRemoteJWTValidator(
    jwks_url=JWKS_URL, audience=AUDIENCE
    ))

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
    user_email = request.user["email"]
    print(request.user["email"])
    return jsonify({"message": f"Hello {user_email}!"})

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)