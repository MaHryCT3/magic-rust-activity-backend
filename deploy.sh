#!/bin/bash

DIRECTORY=/opt/magic-rust-backend-activity/;

cd $DIRECTORY;

docker pull ghcr.io/mahryct3/magic-rust-activity-backend:$CI_COMMIT_SHORT_SHA;

if [[ $? = 0 ]]
    then
      docker compose down;
      docker compose up -d;
    else
      echo "Failed to pull Docker images"
      exit 1
fi