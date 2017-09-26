#!/usr/bin/env bash

geth --datadir=/geth-data --metrics --shh --rpc --rpcaddr 0.0.0.0 --ws --wsaddr 0.0.0.0 --nat none --verbosity 5 --vmdebug --dev --maxpeers 0 --gasprice 0 --debug --pprof
