FROM ubuntu:17.04

RUN \
    apt-get update && \
    apt-get -y -qq upgrade && \
    apt-get -y -qq install \
        build-essential \
        cmake \
        git \
        wget \
        libncurses5-dev \
        libreadline-dev \
        nettle-dev \
        libgnutls28-dev \
        libuv1-dev \
        libmsgpack-dev \
        libargon2-0-dev \
        cython3 \
        python3-dev \
        python3-setuptools \
        libssl-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /jsoncpp

RUN \
    git clone --recursive https://github.com/open-source-parsers/jsoncpp.git && \
    mkdir jsoncpp/build && \
    cd jsoncpp/build && \
    cmake .. \
        -G "Unix Makefiles" \
        && \
    make install


WORKDIR /restbed

RUN \
    git clone --recursive https://github.com/corvusoft/restbed.git && \
    mkdir restbed/build && \
    cd restbed/build && \
    cmake .. \
        -DCMAKE_INSTALL_LIBDIR=/usr/local/lib \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DBUILD_SHARED=On \
        && \
    make install



WORKDIR /opendht

RUN \
    git clone https://github.com/savoirfairelinux/opendht.git && \
	mkdir opendht/build && \
	cd opendht/build && \
	cmake .. \
	    -DOPENDHT_PROXY_SERVER=On \
	    -DOPENDHT_SHARED=Off \
	    && \
	make install && \
	ldconfig

ENTRYPOINT ["dhtnode"]
CMD ["-i",  "-b", "bootstrap.ring.cx:4222",  "-p", "4222", "--proxyserver", "9100"]
