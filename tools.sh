#!/usr/bin/env bash

set -o errexit
#set -o verbose
set -o xtrace
set -o nounset

SN_NETWORK_ACCOUNT_PASSWORD=${SN_NETWORK_ACCOUNT_PASSWORD:=no_password_set}

case "$1" in

init)
    #https://www.vaultproject.io/intro/getting-started/deploy.html#initializing-the-vault+
    ;;

demo)
    docker-compose -f docker-compose.demo.yml create --build --force-recreate demo
    docker-compose -f docker-compose.demo.yml run --service-ports demo ./agent.sh $2
    ;;

dev)
    docker-compose -f docker-compose.dev.yml create --build --force-recreate dev
    docker-compose -f docker-compose.dev.yml run --service-ports dev ./agent.sh run
    ;;

alice)
    docker-compose -f docker-compose.abc.yml create --build --force-recreate alice
    docker-compose -f docker-compose.abc.yml run --service-ports alice ./agent.sh run
    ;;

bob)
    docker-compose -f docker-compose.abc.yml create --build --force-recreate bob
    docker-compose -f docker-compose.abc.yml run --service-ports bob ./agent.sh run
    ;;

charlie)
    docker-compose -f docker-compose.abc.yml create --build --force-recreate charlie
    docker-compose -f docker-compose.abc.yml run --service-ports charlie ./agent.sh run
    ;;

agent-docs)
    docker-compose create --build --force-recreate test
    docker-compose run test ./agent.sh docs
    ;;

agent-test)
    docker-compose start testrpc
    docker-compose create --build test
    docker-compose run test ./agent.sh test
    ;;

agent-web)
    docker-compose run --service-ports agent-web ./agent-web.sh run
    ;;

opendht)
    docker-compose create --build --force-recreate opendht
    docker-compose run --service-ports opendht
    ;;

geth)
    docker-compose create --build --force-recreate geth
    docker-compose run --service-ports geth $2
    ;;

solc)
    docker-compose run --service-ports geth solc --help
    ;;

parity)
    docker-compose -f docker-compose.dev.yml create --build --force-recreate parity
    docker-compose -f docker-compose.dev.yml run --service-ports parity $2
    ;;

vault)
    docker-compose create --build --force-recreate vault
    docker-compose run --service-ports vault $2
    ;;

relex)
    docker-compose -f docker-compose.dev.yml  run --service-ports relex
    ;;

testrpc)
    docker-compose create --build --force-recreate testrpc
    docker-compose run --service-ports testrpc
    ;;

prepare-dao)
    docker-compose -f docker-compose.dao.yml create --build --force-recreate dao
    docker-compose -f docker-compose.dao.yml run --service-ports dao ./dao.sh $2
    ;;

ipfs)
    docker-compose run --service-ports ipfs daemon
    ;;

clean)
    docker-compose down --rmi all --remove-orphans
    ;;

hard-clean)
    docker image prune
    docker-compose down --rmi all --remove-orphans
    docker kill `docker ps -q` || true
    docker rm `docker ps -a -q`
    docker rmi `docker images -q`
    docker volume rm `docker volume ls -qf dangling=true`
    ;;

create-web-cookie)
    docker-compose run agent-web-cookie
    ;;

gen-ssl)
    cd agent
    openssl req -nodes -new -x509  -keyout server.key -out server.crt -subj '/CN=localhost'
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
