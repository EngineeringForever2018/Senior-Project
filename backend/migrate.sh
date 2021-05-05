pwd
ls -a
source .env.local
./cloud_sql_proxy -credential_file=service-key.json -instances=$SQL_CONNECTION_NAME=tcp:5432 &
python manage.py migrate --settings=backend.settings.production
