FROM ubuntu:17.04

RUN \
       apt-get update \
    && apt-get install -y \
                            apt-utils \
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
                            libssl-dev \
                            net-tools \
                            nmap \
    && apt-get dist-upgrade -y \
    && apt-get clean

RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz \
    && tar xfzv Python-3.6.3.tgz \
    && cd Python-3.6.3 \
    && ./configure \
    && make \
    && make install \
    && pip3 install cython

RUN git clone --branch 1.3.6 https://github.com/savoirfairelinux/opendht.git \
	&& cd opendht \
	&& mkdir build \
	&& cd build \
	&& cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DOPENDHT_PYTHON=On -DOPENDHT_LTO=On \
	&& make -j8 \
	&& make install \
	&& cd ../.. \
	&& rm -rf opendht

ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements.txt /code
RUN pip3 install -r requirements.txt

ADD . /code
