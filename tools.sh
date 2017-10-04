#!/usr/bin/env bash

set -o errexit
set -o verbose
set -o xtrace
set -o nounset

function recreate_agent_image {
    docker-compose create --build --force-recreate agent
}

case "$1" in

demo)
    docker-compose up --build --force-recreate
    ;;

agent)
    recreate_agent_image
    docker-compose run --service-ports agent ./agent.sh run
    ;;

agent-docs)
    recreate_agent_image
    docker-compose run agent ./agent.sh docs
    ;;

agent-test)
    recreate_agent_image
    docker-compose run agent ./agent.sh test
    ;;

agent-web)
    docker-compose run --service-ports agent-web ./agent-web.sh run
    ;;

geth)
    docker-compose run --service-ports geth geth --datadir=/geth-data --metrics --shh --rpc --rpcaddr 0.0.0.0 --ws --wsaddr 0.0.0.0 --nat none --verbosity 5 --vmdebug --dev --maxpeers 0 --gasprice 0 --debug --pprof
    ;;

solc)
    docker-compose run --service-ports geth solc --help
    ;;

parity)
    docker-compose run --service-ports parity parity --help
    ;;

truffle)
    docker-compose run --service-ports truffle truffle --help
    ;;

clean)
    docker-compose down --rmi all --remove-orphans
    ;;

hard-clean)
    docker-compose down --rmi all --remove-orphans
    docker kill `docker ps -q`
    docker rm `docker ps -a -q`
    docker rmi `docker images -q`
    docker volume rm `docker volume ls -qf dangling=true`
    ;;

create-web-cookie)
    docker-compose run agent-web-cookie
    ;;



*) echo 'No operation specified'
    exit 0;
    ;;

esac
