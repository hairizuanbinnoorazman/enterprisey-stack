from flask import Flask, request, jsonify
import jwt, requests

app = Flask(__name__)

DEX_URL = "http://127.0.0.1:5556"
JWKS_URL = f"{DEX_URL}/keys"
AUDIENCE = "flask"  # same as in your token

jwks = requests.get(JWKS_URL).json()
public_keys = {
    key["kid"]: jwt.algorithms.RSAAlgorithm.from_jwk(key)
    for key in jwks["keys"]
}

def verify_token(token):
    headers = jwt.get_unverified_header(token)
    print(headers)
    key = public_keys[headers["kid"]]
    return jwt.decode(token, key=key, audience=AUDIENCE, algorithms=["RS256"])

@app.before_request
def check_auth():
    if request.path == "/health":
        return
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Missing bearer token"}), 401
    token = auth.split()[1]
    try:
        claims = verify_token(token)
        request.user = claims
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route("/api/resource")
def resource():
    user_email = request.user["email"]
    print(request.user["email"])
    return jsonify({"message": f"Hello {user_email}!"})

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)