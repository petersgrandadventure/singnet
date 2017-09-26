#!/usr/bin/env bash

set -o errexit
set -o verbose
set -o xtrace
set -o nounset

case "$1" in

up)
    docker-compose up --build --force-recreate
    ;;

run)
    docker-compose run agent run
    ;;

clean)
    docker-compose down --rmi all --remove-orphans
    ;;

hard-clean)
    docker-compose down --rmi all --remove-orphans
    docker ps -q | xargs -r docker kill
    docker ps -a -q | xargs -r docker rm
    docker images -q | xargs -r docker rmi
    docker volume ls -qf dangling=true | xargs -r docker volume rm
    ;;

create-web-cookie)
    docker-compose run agent-web-cookie
    ;;

docs)
    docker-compose create --build --force-recreate agent
    docker-compose run agent docs
    ;;

test)
    docker-compose create --build --force-recreate agent
    docker-compose run agent test
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
