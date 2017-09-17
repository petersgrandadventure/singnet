# Docker Info

You will need docker and docker-compose installed:

https://docs.docker.com/engine/installation/
https://docs.docker.com/compose/install/

The general concept is 1 Dockerfile per process (i.e. Agent) or tool (i.e. Truffle)

./docker-tools.sh run will recreate all the images and run a functioning demo set.

Once the docker-compose is up, the exposed ports are:
8000 = agent
8080 = agent web
8545 = Geth JSON-RPC
8546 = Geth Websocket
