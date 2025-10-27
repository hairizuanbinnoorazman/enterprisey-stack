from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__)
app.secret_key = "secret-key"

oauth = OAuth(app)
keycloak = oauth.register(
    name="Flask App",
    client_id=os.getenv("OIDC_CLIENT_ID"),
    client_secret=os.getenv("OIDC_CLIENT_SECRET"),
    server_metadata_url=f"{os.getenv('OIDC_ISSUER')}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile offline_access",
        "token_endpoint_auth_method": "client_secret_basic",
    },
)

@app.route("/")
def home():
    user = session.get("user")
    if user:
        # return f"Hello, {user['email']}!"
        return render_template("main.html", name=user['email'])
    return '<a href="/login">Login</a>'

@app.route("/login")
def login():
    redirect_uri = url_for("auth", _external=True)
    return keycloak.authorize_redirect(redirect_uri)

@app.route("/testtest")
def testtest():
    print(session["token"])
    lol = requests.get("http://localhost:5001/api/resource", headers={
        "Authorization": f"Bearer {session['token']['access_token']}",
    })
    print(lol.text)
    return lol.text

@app.route("/auth")
def auth():
    # Exchange authorization code for token (Authorization Code Flow)
    token = keycloak.authorize_access_token()
    # token contains access_token, id_token, etc.
    id_token = token.get("id_token")
    userinfo = token.get("userinfo") or token
    session["user"] = userinfo
    session["token"] = token
    print(userinfo)
    print(token)
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
