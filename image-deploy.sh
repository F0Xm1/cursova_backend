#!/bin/bash
set -x

mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keyscan -H 35.225.117.203 >> ~/.ssh/known_hosts

ssh ubuntu@35.225.117.203 "sudo users" || true

export DOCKER_HOST=ssh://ubuntu@35.225.117.203

docker compose build backend
docker compose up -d backend

echo "Checking status"
docker compose ps

echo "Deployed successfully"