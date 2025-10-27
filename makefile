
app:
	OIDC_CLIENT_ID=flask OIDC_CLIENT_SECRET=flask-secret OIDC_ISSUER=http://localhost:5556 python main.py

ultimate:
	python ultimate.py

check:
	curl -H "Authorization: Bearer XXX.XXX.XXX" localhost:5001/api/resource