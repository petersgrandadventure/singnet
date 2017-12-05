#!/usr/bin/env sh

set -o errexit
set -o verbose
set -o xtrace
set -o nounset


case "$1" in

noop)
    ;;

bash)
    /bin/bash
    ;;

run)
    truffle compile
    truffle migrate --reset
    truffle test
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
