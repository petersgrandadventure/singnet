import logging
import opendht as dht

import bson

logger = logging.getLogger(__name__)


class DHT:
    def __init__(self, boot_host, boot_port):

        node = dht.DhtRunner()
        self.node = node

        node.run()

        node.bootstrap(boot_host, boot_port)

    def put(self, key, value, value_id=None, type_id=None):
        logger.debug('Putting key and value into DHT: %s - %s', key, value)

        value_bin = bson.dumps(value)

        key_hash = dht.InfoHash.get(key)
        connection_data = dht.Value(value_bin)

        if value_id:
            connection_data.id = value_id

        if type_id:
            connection_data.user_type = type_id

        self.node.put(key_hash, connection_data)

        logger.debug('key and value put into DHT')

    def get(self, key):
        logger.debug('Getting data info for key: %s', key)

        key_hash = dht.InfoHash.get(key)
        data_bin = self.node.get(key_hash)

        data = []

        # Deserialize from BSON - another serializer could be used but BSON works well here
        for d in data_bin:
            data = bson.loads(d.data)
            data.append(data)

        logger.debug('Key Value info: %s', data)
        return data
