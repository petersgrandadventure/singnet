#!/usr/bin/env bash

set -o errexit
set -o nounset

export SN_NETWORK_GATEWAY=$(netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}') || true
echo $SN_NETWORK_GATEWAY

case "$1" in

noop)
    ;;

run)
    export PYTHONPATH=/code
    python3 sn_agent/cli.py run
    ;;

docs)
    cd docs
    make html
    ;;

test)
    export PYTHONPATH=/code
    export SN_SERVICE_ADAPTER_CONFIG_FILE=/code/tests/test_config.yml
    export SN_AGENT_ID=b545478a-971a-48ec-bc56-4b9b7176799c
    py.test --verbose --cov-config .coveragerc --cov-report html --cov=sn_agent tests
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
