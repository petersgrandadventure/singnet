#!/usr/bin/env bash

set -o errexit
set -o verbose
set -o xtrace
set -o nounset

# download, compile and install python: https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
# download, decompress node:

# sudo apt install build-essential cmake libboost-all-dev libz3-dev libcupti-dev

BASE_DIR=${PWD}
AGENT_DIR=${BASE_DIR}/agent
AGENT_SRC_DIR=${AGENT_DIR}/src
INSTALL_DIR=${BASE_DIR}/local
PYTHON2_DIR=${INSTALL_DIR}/python2
PYTHON2_BIN_DIR=${INSTALL_DIR}/python2/bin
PYTHON2=${PYTHON2_DIR}/bin/python2

PYTHON3_DIR=${INSTALL_DIR}/python3
PYTHON3=${PYTHON3_DIR}/bin/python3
PIP3=${PYTHON3_DIR}/bin/pip3
VENV=${INSTALL_DIR}/venv
VENV_BIN_DIR=${VENV}/bin
VPYTHON3=${VENV}/bin/python3

NODE_DIR=${INSTALL_DIR}/node
NODE=${NODE_DIR}/bin/node
NPM=${NODE_DIR}/bin/npm
NODE_MODULES=${AGENT_DIR}/node_modules
VENDOR=${AGENT_SRC_DIR}/sn_agent_ui/static/vendor

RUBY_DIR=${INSTALL_DIR}/ruby
RUBY=${RUBY_DIR}/bin/ruby
GEM=${RUBY_DIR}/bin/gem
SCSS=${RUBY_DIR}/bin/scss

REDIS_DIR=${INSTALL_DIR}/redis
REDIS=${REDIS_DIR}/bin/redis-server

GETH=${INSTALL_DIR}/geth/geth
SOLC=${INSTALL_DIR}/solidity-src/build/solc/solc

function ensure_root {
    # Make sure only root can run our script
    if [[ $EUID -ne 0 ]]; then
       echo "This script must be run as root" 1>&2
       exit 1
    fi
}

function system_prep {
    ensure_root
    apt install build-essential cmake libboost-all-dev libz3-dev libcupti-dev zlib1g-dev g++ libssl-dev
}

function install_docker {
    ensure_root

    #https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
    apt-get remove docker docker-engine docker.io
    apt-get update
    apt-get install apt-transport-https ca-certificates curl software-properties-common linux-image-extra-$(uname -r) linux-image-extra-virtual
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    apt-key fingerprint 0EBFCD88
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-get install docker-ce
}

function create_docs {
    ${VENV_BIN_DIR}/sphinx-build -b dirhtml "${AGENT_DIR}/docs/" "${AGENT_DIR}/docs/_build"
#    make html
#    make coverage
    cd ..
}

function run_tests {
    cd ${AGENT_DIR}
    ${VENV}/bin/tox
}

function remove_all_docker {
    docker-compose down --rmi all --remove-orphans
}

function run_compose {
    docker-compose up --force-recreate
}

case "$1" in

clean)
    remove_all_docker
    ;;

system-prep)
    system_prep
    ;;

install_docker)
    install_docker
    ;;

run)
    run_compose
    ;;

cookie)
    cd ${AGENT_SRC_DIR}
    PYTHONPATH=${AGENT_SRC_DIR} ${VPYTHON3} sn_agent/session.py
    ;;

docs)
    create_docs
    ;;

test)
    run_tests
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
