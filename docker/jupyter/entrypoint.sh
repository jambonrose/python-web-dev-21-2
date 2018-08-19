#!/usr/bin/env sh

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

python3.7 manage.py shell_plus --notebook
