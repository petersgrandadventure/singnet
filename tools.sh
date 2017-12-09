#!/usr/bin/env bash

set -o errexit
#set -o verbose
#set -o xtrace
set -o nounset

SN_NETWORK_ACCOUNT_PASSWORD=${SN_NETWORK_ACCOUNT_PASSWORD:=no_password_set}
export SN_NETWORK_ACCOUNT_PASSWORD

case "$1" in

init)
    #https://www.vaultproject.io/intro/getting-started/deploy.html#initializing-the-vault+
    ;;

demo)
    docker-compose -f docker/docker-compose.demo.yml create --build --force-recreate demo
    docker-compose -f docker/docker-compose.demo.yml run --service-ports demo ./agent.sh run
    ;;

demo-down)
    docker-compose -f docker/docker-compose.demo.yml down --remove-orphans
    ;;

deploy-contracts)
    DOCKERNET=$(docker network ls | grep dockernet | awk '{print $2}')
    if [ "$DOCKERNET" != "dockernet" ]
    then
        echo "Starting docker network: dockernet"
        docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
    else
        echo "Docker network 'dockernet' already running."
    fi
    echo ""
    HOST_OS=$(uname)
    echo "HOST_OS = '$HOST_OS'"
    if [ "$HOST_OS" == "Darwin" ]
    then
        echo "Using Truffle network - docker_host_mac"
        TRUFFLE_NETWORK=docker_host_mac
    else
        echo "Using Truffle network - docker_host"
        TRUFFLE_NETWORK=docker_host
    fi
    export TRUFFLE_NETWORK
    echo "TRUFFLE_NETWORK = '$TRUFFLE_NETWORK'"
    docker-compose -f docker/docker-compose.dev.yml create --build --force-recreate truffle
    docker-compose -f docker/docker-compose.dev.yml run --service-ports truffle
    ;;

dev)
    docker-compose -f docker/docker-compose.dev.yml create --build dev
    docker-compose -f docker/docker-compose.dev.yml run --service-ports dev ./agent.sh run
    ;;

dev-force-build)
    docker-compose -f docker/docker-compose.dev.yml create --build --force-recreate dev
    ;;

dev-build)
    docker-compose -f docker/docker-compose.dev.yml create --build dev
    ;;

dev-run)
    docker-compose -f docker/docker-compose.dev.yml run --service-ports dev ./agent.sh run
    ;;

dev-down)
    docker-compose -f docker/docker-compose.dev.yml down --remove-orphans
    ;;

alice)
    docker-compose -f docker/docker-compose.abc.yml create --build --force-recreate alice
    docker-compose -f docker/docker-compose.abc.yml run --service-ports alice ./agent.sh run
    ;;

bob)
    docker-compose -f docker/docker-compose.abc.yml create --build --force-recreate bob
    docker-compose -f docker/docker-compose.abc.yml run --service-ports bob ./agent.sh run
    ;;

charlie)
    docker-compose -f docker/docker-compose.abc.yml create --build --force-recreate charlie
    docker-compose -f docker/docker-compose.abc.yml run --service-ports charlie ./agent.sh run
    ;;

agent-docs)
    docker-compose -f docker/docker-compose.yml create --build --force-recreate test
    docker-compose -f docker/docker-compose.ymlrun test ./agent.sh docs
    ;;

agent-test)
    docker-compose -f docker/docker-compose.yml start testrpc
    docker-compose -f docker/docker-compose.yml create --build test
    docker-compose -f docker/docker-compose.yml run test ./agent.sh test
    ;;

opendht)
    docker-compose -f docker/docker-compose.yml create --build --force-recreate opendht
    docker-compose -f docker/docker-compose.yml run --service-ports opendht
    ;;

geth)
    docker-compose -f docker/docker-compose.yml create --build --force-recreate geth
    docker-compose -f docker/docker-compose.yml run --service-ports geth $2
    ;;

solc)
    docker-compose -f docker/docker-compose.yml run --service-ports geth solc --help
    ;;

parity)
    docker-compose -f docker-compose.dev.yml create --build --force-recreate parity
    docker-compose -f docker-compose.dev.yml run --service-ports parity $2
    ;;

vault)
    docker-compose -f docker/docker-compose.yml create --build --force-recreate vault
    docker-compose -f docker/docker-compose.yml run --service-ports vault $2
    ;;

relex)
    docker-compose -f docker/docker-compose.dev.yml  run --service-ports relex
    ;;

testrpc)
    docker-compose -f docker/docker-compose.yml create --build --force-recreate testrpc
    docker-compose -f docker/docker-compose.yml run --service-ports testrpc
    ;;

prepare-dao)
    docker-compose -f docker-compose.dao.yml create --build --force-recreate dao
    docker-compose -f docker-compose.dao.yml run --service-ports dao ./dao.sh $2
    ;;

ipfs)
    docker-compose -f docker/docker-compose.yml run --service-ports ipfs daemon
    ;;

clean)
    docker-compose -f docker/docker-compose.yml down --rmi all --remove-orphans
    ;;

hard-clean)
    docker image prune
    docker-compose -f docker/docker-compose.dev.yml down --rmi all --remove-orphans
    docker-compose -f docker/docker-compose.yml down --rmi all --remove-orphans
    docker kill `docker ps -q` || true
    docker rm `docker ps -a -q`
    docker rmi `docker images -q`
    docker volume rm `docker volume ls -qf dangling=true`
    ;;

create-web-cookie)
    docker-compose -f docker/docker-compose.yml run agent-web-cookie
    ;;

gen-ssl)
    cd agent
    openssl req -nodes -new -x509  -keyout server.key -out server.crt -subj '/CN=localhost'
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
