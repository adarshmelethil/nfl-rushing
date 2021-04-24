#!/usr/bin/env bash
set -euo pipefail

POSTGRES_DB=${POSTGRES_DB:-nfl}
POSTGRES_USER=${POSTGRES_USER:-nfl}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-nfl}
exec psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
