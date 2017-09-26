#!/usr/bin/env bash

set -o errexit
set -o nounset


case "$1" in

noop)
    ;;

run)
    geth --datadir=/geth-data --metrics --shh --rpc --rpcaddr 0.0.0.0 --ws --wsaddr 0.0.0.0 --nat none --verbosity 5 --vmdebug --dev --maxpeers 0 --gasprice 0 --debug --pprof
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
