FROM ubuntu:17.04

ENV DEBIAN_FRONTEND noninteractive

RUN \
    apt-get update && \
    apt-get -y -qq upgrade && \
    apt-get -y -qq install software-properties-common && \
    add-apt-repository ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get -y -qq install geth solc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /geth
COPY geth.sh .
COPY config.toml .
COPY password.txt .

ENTRYPOINT ["/geth/geth.sh"]
CMD ["run"]
