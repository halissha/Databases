#!/bin/bash

printf "Creating Redis container . . .\n"
docker rm -f c_redis || true
docker run -d --name "c_redis" -p 27015:6379 redis

printf "\nCreating MongoDB container . . .\n"
docker rm -f c_mongo || true
docker run -d --name "c_mongo" -p 27016:27017 mongo

printf "\nCreating Neo4j container . . .\n"
docker rm -f c_neo4j || true
docker run -d --name "c_neo4j" -p 27017:7474 --env NEO4J_AUTH=neo4j/zx3021 neo4j

printf "\nCreating ElasticSearch 6.5.0 container . . .\n"
docker rm -f c_elastic || true
docker run -d --name "c_elastic" -p 27018:9200 elasticsearch:6.5.0

printf "\nCreating PostgreSQL container . . .\n"
docker rm -f c_psql || true
docker run -d --name "c_psql" -p 27019:5432 -e POSTGRES_PASSWORD=zx3021 postgres
