#!/bin/sh 

mkdir -p nginx/log

export TMPDIR=/private$TMPDIR
export LOCALSTACK_API_KEY=my-localstack-key

docker-compose build 
docker-compose up 
