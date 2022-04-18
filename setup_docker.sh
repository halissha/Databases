#!/bin/bash

printf "Installing Redis . . .\n"
docker pull redis

printf "\nInstalling MongoDB . . .\n"
docker pull mongo

printf "\nInstalling Neo4j . . .\n"
docker pull neo4j

printf "\nInstalling ElasticSearch 6.5.0 . . .\n"
docker pull elasticsearch:6.5.0

printf "\nInstalling PostgreSQL . . .\n"
docker pull postgres



