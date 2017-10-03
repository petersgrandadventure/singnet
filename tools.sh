#!/usr/bin/env bash

set -o errexit
set -o verbose
set -o xtrace
set -o nounset

function recreate_agent_image {
    docker-compose create --build --force-recreate agent
    docker-compose create --build --force-recreate agent2
}

case "$1" in

demo)
    docker-compose up --build --force-recreate
    ;;

agent)
    recreate_agent_image
    docker-compose run --service-ports agent ./agent.sh run
    ;;

agent2)
    recreate_agent_image
    docker-compose run --service-ports agent2 ./agent.sh run
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
    docker-compose run --service-ports parity
    ;;

truffle)
    docker-compose run --service-ports truffle
    ;;

ipfs)
    docker-compose run --service-ports ipfs daemon
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

gen-ssl)
    openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
    openssl rsa -passin pass:x -in server.pass.key -out server.key
    rm server.pass.key
    openssl req -new -key server.key -out server.csr -subj "/C=UK/ST=Warwickshire/L=Leamington/O=OrgName/OU=IT Department/CN=example.com"
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
