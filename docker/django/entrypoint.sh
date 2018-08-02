#!/usr/bin/env sh

if [ "$#" = 0 ]
then
    python3.7 -m pip freeze
fi

postgres_ready() {
python3.7 << END
from sys import exit
from psycopg2 import connect, OperationalError
try:
    connect(
        dbname="$POSTGRES_DB",
        user="$POSTGRES_USER",
        password="$POSTGRES_PASSWORD",
        host="postgres",
    )
except OperationalError as error:
    print(error)
    exit(-1)
exit(0)
END
}

until postgres_ready; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 3
done;

>&2 echo "Postgres is available"

if [ "$#" = 0 ]
then
    >&2 echo "No command detected; running default commands"
    >&2 echo "Running migrations"
    python3.7 manage.py migrate --noinput
    >&2 echo "\n\nStarting development server: 127.0.0.1:8000\n\n"
    python3.7 manage.py runserver 0.0.0.0:8000
else
    >&2 echo "Command detected; running command"
    exec "$@"
fi
