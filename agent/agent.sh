#!/usr/bin/env bash

set -o errexit
set -o nounset

export SN_AGENT_WEB_HOST=$(netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}')

function run_tests {
    py.test --verbose --cov-config .coveragerc --cov-report html --cov=sn_agent tests
}

case "$1" in

noop)
    ;;

run)
    python3 agent.py
    ;;

docs)
    cd docs
    make html
    ;;

test)
    run_tests
    ;;


*) echo 'No operation specified'
    exit 0;
    ;;

esac
