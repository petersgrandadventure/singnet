FROM node:8

WORKDIR /dao

COPY package.json .

RUN \
    npm install -g truffle && \
    npm install

COPY . .

