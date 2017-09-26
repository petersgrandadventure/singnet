#!/usr/bin/env bash

set -o errexit
set -o nounset

function run_tests {
    py.test --verbose --cov-config .coveragerc --cov-report html --cov=sn_agent tests
}

case "$1" in

noop)
    ;;

run)
    python agent-web.py
    ;;

docs)
    cd docs
    make html
    ;;

test)
    run_tests
    ;;

travis-test)
    run_tests
    coveralls
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
