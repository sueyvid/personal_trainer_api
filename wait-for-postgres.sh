#!/bin/sh
# wait-for-postgres.sh

set -e

host="$PGHOST"

until pg_isready -h "$host" -U "postgres" -q; do
  >&2 echo "Postgres ainda não está pronto - esperando..."
  sleep 1
done

>&2 echo "Postgres está pronto - executando o comando principal"
exec "$@"