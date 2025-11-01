-include .env
export

app:
	python main.py

ultimate:
	python ultimate.py

check:
	curl -H "Authorization: Bearer XXX.XXX.XXX" localhost:5001/api/resource

env:
	# For authentik
	# Probably cannot be run via make, we need to copy and run it on bash/shell
	echo "PG_PASS=$(openssl rand -base64 36 | tr -d '\n')" >> .env
	echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 60 | tr -d '\n')" >> .env
	echo "AUTHENTIK_ERROR_REPORTING__ENABLED=true" >> .env
	echo "AUTHENTIK_BOOTSTRAP_PASSWORD=admin" >> .env