#!/usr/bin/env bash
set -euo pipefail

source env.sh

exec psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
