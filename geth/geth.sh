#!/usr/bin/env bash

set -o errexit
set -o nounset

case "$1" in

noop)
    ;;

create-account)
    geth --config config.toml account new
    ;;

run)
    geth --rpcapi admin,eth,web3,personal,net,shh,
    db --rpc --config config.toml --password password.txt --unlock 0
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
