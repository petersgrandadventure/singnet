#!/usr/bin/env sh

set -o errexit
set -o nounset


case "$1" in

noop)
    ;;

run)
    parity --help
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
