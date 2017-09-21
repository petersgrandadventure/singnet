FROM parity

ENV DEBIAN_FRONTEND noninteractive

RUN \
apt-get update && \
apt-get -y -qq dist-upgrade && \
apt-get -y -qq install software-properties-common && \
apt-get clean && \
rm -rf /var/lib/apt/lists/* && \
bash <(curl https://get.parity.io -L)
