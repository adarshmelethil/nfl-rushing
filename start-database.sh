#!/usr/bin/env bash
set -euo pipefail

VOLUME_NAME=nfl_data

source env.sh

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -v|--volume)
            VOLUME_NAME="$2"
            shift; shift;
            ;;
        -d|--database)
            POSTGRES_DB="$2"
            shift; shift;
            ;;
        -p|--password)
            POSTGRES_PASSWORD="$2"
            shift; shift;
            ;;
        -u|--user)
            POSTGRES_USER="$2"
            shift; shift;
            ;;
        --help)
            echo "Run postgres in a container with consistent volume"
            exit 1
            ;;
        *)
            exit 2
            ;;
    esac
done


docker volume create ${VOLUME_NAME}
exec docker run --rm -iu --name rushing-db \
    --mount "type=volume,source=${VOLUME_NAME},target=/var/lib/postgresql/data" \
    --publish 5432:5432 \
    --env POSTGRES_DB=${POSTGRES_DB} \
    --env POSTGRES_USER=${POSTGRES_USER} \
    --env POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
    postgres:9.6.17-alpine
