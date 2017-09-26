#!/usr/bin/env bash

set -o errexit
set -o verbose
set -o xtrace
set -o nounset

case "$1" in

run)
    ls -lar
    ;;

--help)
    echo 'Executing in the default context, specify "run" to actually execute'
    ;;

*) echo 'No operation specified'
    exit 0;
    ;;

esac
