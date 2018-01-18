FROM parity/parity:stable

WORKDIR /parity
COPY config.toml .
COPY parity.sh .

ENTRYPOINT ["/parity/parity.sh"]
CMD ["run"]

