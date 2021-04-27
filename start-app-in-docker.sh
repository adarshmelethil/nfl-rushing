#!/usr/bin/env bash
set -euo pipefail

# NOTE: Make sure the database is running using start-database.sh script

source env.sh

RUSHING_IMAGE=rushing
docker build -t ${RUSHING_IMAGE} .

# Create a network with the database already connected
docker network create rushing-network || :
docker network connect rushing-network rushing-db || :

COMMON_FLAGS=(
    --rm
    -it
    --env POSTGRES_DB=${POSTGRES_DB}
    --env POSTGRES_USER=${POSTGRES_USER}
    --env POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    --env POSTGRES_HOST=rushing-db
    --env POSTGRES_PORT=5432
    --env FLASK_APP=${FLASK_APP}
    --network rushing-network
)



# Show Data From file
docker run \
    ${COMMON_FLAGS[@]} \
    --name rushing-migration \
    ${RUSHING_IMAGE} \
    rushing data show

# Run Database migrations
docker run \
    ${COMMON_FLAGS[@]} \
    --name rushing-migration \
    ${RUSHING_IMAGE} \
    flask db upgrade

# Upload data
docker run \
    ${COMMON_FLAGS[@]} \
    --name rushing-migration \
    ${RUSHING_IMAGE} \
    rushing data load

# Run server
server_port=8080
docker run \
    ${COMMON_FLAGS[@]} \
    --name rushing-migration \
    --publish ${server_port}:${server_port} \
    ${RUSHING_IMAGE} \
    rushing server start --host="0.0.0.0" --port="${server_port}"
