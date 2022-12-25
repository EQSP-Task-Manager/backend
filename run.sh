#!/bin/bash

set -eu

# wait for db container to start
sleep 5

# apply migration and start api
DB_URL="postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@task-manager-db:5432/task-manager"
task-manager-db --db-url ${DB_URL} upgrade head
task-manager-api
