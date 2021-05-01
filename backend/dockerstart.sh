#! /bin/bash
source .env.local

./cloud_sql_proxy -credential_file=service-key.json -instances=$SQL_CONNECTION_NAME=tcp:5432 &

# Gunicorn listens on 127.0.0.1 by default, which isn't for docker (172.17.0.1).
# Changing this to 0.0.0.0 allows it to serve all interfaces, including docker.
gunicorn backend.wsgi -b 0.0.0.0:8000
