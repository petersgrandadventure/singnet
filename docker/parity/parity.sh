#!/usr/bin/env bash

set -o errexit
set -o nounset

case "$1" in

noop)
    ;;

create-account)
    ./parity --config config.toml account new
    ;;

run)
    ./parity --config config.toml
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
