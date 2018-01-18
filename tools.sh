#!/usr/bin/env bash

set -o errexit
#set -o verbose
#set -o xtrace
set -o nounset

SN_NETWORK_ACCOUNT_PASSWORD=${SN_NETWORK_ACCOUNT_PASSWORD:=no_password_set}
export SN_NETWORK_ACCOUNT_PASSWORD

case "$1" in

# Deploys the Smart Contracts in agent/sn_agent/network/ethereum/core to the specififed network via a
# dockerized version of the Truffle environment and copies the compiled code and deployed addresses to
# the docker/agent/data/dev directory where the Agent's web3.py network class can find it.
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
    docker-compose -f docker/docker-compose.dev.yml create --build truffle
    docker-compose -f docker/docker-compose.dev.yml run --service-ports truffle
    ;;

# The main developer command for testing and bring up a developer agent
dev)
    docker-compose -f docker/docker-compose.dev.yml create --build dev
    docker-compose -f docker/docker-compose.dev.yml run --service-ports dev ./agent.sh run
    ;;

# Rebuilds the dev image in case of stale docker caches
dev-force-build)
    docker-compose -f docker/docker-compose.dev.yml create --build --force-recreate dev
    ;;

# Builds the image only but does not run ig
dev-build)
    docker-compose -f docker/docker-compose.dev.yml create --build dev
    ;;

# Just run the built image.
dev-run)
    docker-compose -f docker/docker-compose.dev.yml run --service-ports dev ./agent.sh run
    ;;

# Take down all the dev containers - defined in docker/docker-compose-dev.yml
dev-down)
    docker-compose -f docker/docker-compose.dev.yml down --remove-orphans
    ;;


# ABC - Alice, Bob and Charlie (she's a girl)

# Brings up the Alice server fo demonstrate many agents interacting.
alice)
    docker-compose -f docker/docker-compose.abc.yml create --build alice
    docker-compose -f docker/docker-compose.abc.yml run --service-ports alice ./agent.sh run
    ;;

# Brings up Bob
bob)
    docker-compose -f docker/docker-compose.abc.yml create --build bob
    docker-compose -f docker/docker-compose.abc.yml run --service-ports bob ./agent.sh run
    ;;

# Brings up Charlie - she likes to be last...
charlie)
    docker-compose -f docker/docker-compose.abc.yml create --build charlie
    docker-compose -f docker/docker-compose.abc.yml run --service-ports charlie ./agent.sh run
    ;;

 demo)
    docker-compose -f docker/docker-compose.demo.yml create --build --force-recreate demo
    docker-compose -f docker/docker-compose.demo.yml run --service-ports demo ./agent.sh run
    ;;

demo-down)
    docker-compose -f docker/docker-compose.demo.yml down --remove-orphans
    ;;


# Experimental code - don't count on this staying around

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

ipfs)
    docker-compose -f docker/docker-compose.yml run --service-ports ipfs daemon
    ;;

init)
    #https://www.vaultproject.io/intro/getting-started/deploy.html#initializing-the-vault+
    ;;

# Support

# Builds the docs
agent-docs)
    docker-compose -f docker/docker-compose.yml create --build test
    docker-compose -f docker/docker-compose.ymlrun test ./agent.sh docs
    ;;

# Runs the test suite
agent-test)
    docker-compose -f docker/docker-compose.yml start testrpc
    docker-compose -f docker/docker-compose.yml create --build test
    docker-compose -f docker/docker-compose.yml run test ./agent.sh test
    ;;

# Brings up the OpenCog relationship extracter node
relex)
    docker-compose -f docker/docker-compose.dev.yml  run --service-ports relex
    ;;

# A test Ethereum client RPC server (ganache-cli) docker image
testrpc)
    docker-compose -f docker/docker-compose.yml create --build testrpc
    docker-compose -f docker/docker-compose.yml run --service-ports testrpc
    ;;

# Cleans recent docker images... useful when working on docker-compose and Dockerfiles
clean)
    docker-compose -f docker/docker-compose.yml down --rmi all --remove-orphans
    ;;

# Clears the entire docker cache - generally only necessary when doing work with Dockerfiles themselves
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

*) echo "Command '$1' not found - No operation specified"
    exit 0;
    ;;

esac
