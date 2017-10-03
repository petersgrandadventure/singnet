import logging
import random
import threading
import time

import nacl.encoding
import nacl.signing

from .handler import DHTRequestHandler
from .server import DHTServer
from .settings import DHTSettings
from .bucketset import BucketSet
from .hashing import hash_function, random_id
from .peer import Peer
from .shortlist import Shortlist

logger = logging.getLogger(__name__)


class DHT(object):
    def __init__(self, host=None, port=None, key=None, my_id=None):
        self.settings = DHTSettings()

        if not my_id:
            my_id = random_id()

        if not host:
            host = "0.0.0.0"

        if not port:
            port = random.randint(5000, 10000)

        if not key:
            key = nacl.signing.SigningKey.generate()
        self.my_key = key

        self.peer = Peer(host, port, my_id)
        self.data = {}
        self.buckets = BucketSet(self.settings.K, self.settings.ID_BITS, self.peer.id)
        self.rpc_ids = {}  # should probably have a lock for this

        self.server = DHTServer(self.peer.address(), DHTRequestHandler)
        self.server.dht = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        if self.settings.USE_UPNP:
            self.server.try_upnp_portmap(port)

        if self.settings.NEEDS_BOOTING:
            self.is_boot_node = False
            self.bootstrap(self.settings.BOOT_HOST, self.settings.BOOT_PORT)
        else:
            self.is_boot_node = True

        logger.debug('DHT Server started')

    def iterative_find_nodes(self, key, boot_peer=None):
        logger.debug('Finding nearest nodes...')
        shortlist = Shortlist(self.settings.K, key)
        shortlist.update(self.buckets.nearest_nodes(key))

        if boot_peer:
            logger.debug('This node a boot node: %s', boot_peer)
            rpc_id = random.getrandbits(self.settings.ID_BITS)
            self.rpc_ids[rpc_id] = shortlist
            boot_peer.find_node(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id)

        while (not shortlist.complete()) or boot_peer:
            nearest_nodes = shortlist.get_next_iteration(self.settings.ALPHA)
            for peer in nearest_nodes:
                logger.debug('Nearest Node: %s', peer)
                shortlist.mark(peer)
                rpc_id = random.getrandbits(self.settings.ID_BITS)
                self.rpc_ids[rpc_id] = shortlist
                peer.find_node(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id)
            time.sleep(self.settings.ITERATION_SLEEP)
            boot_peer = None

        return shortlist.results()

    def iterative_find_value(self, key):
        shortlist = Shortlist(self.settings.K, key)
        shortlist.update(self.buckets.nearest_nodes(key))
        while not shortlist.complete():
            nearest_nodes = shortlist.get_next_iteration(self.settings.ALPHA)
            for peer in nearest_nodes:
                shortlist.mark(peer)
                rpc_id = random.getrandbits(self.settings.ID_BITS)
                self.rpc_ids[rpc_id] = shortlist
                peer.find_value(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id)
            time.sleep(self.settings.ITERATION_SLEEP)
        return shortlist.completion_result()

    def bootstrap(self, boot_host, boot_port):
        boot_peer = Peer(boot_host, boot_port, 0)
        self.iterative_find_nodes(self.peer.id, boot_peer=boot_peer)

    def __getitem__(self, key, bypass=0):
        hashed_key = hash_function(key.encode("ascii"))
        if hashed_key in self.data:
            return self.data[hashed_key]["content"]
        result = self.iterative_find_value(hashed_key)
        if result:
            return result["content"]

        raise KeyError

    def __setitem__(self, key, content):
        content = str(content)
        hashed_key = hash_function(key.encode("ascii"))
        nearest_nodes = self.iterative_find_nodes(hashed_key)
        value = {
            "content": content,
            "key": self.my_key.verify_key.encode(encoder=nacl.encoding.Base64Encoder).decode("utf-8"),
            "signature": nacl.encoding.Base64Encoder.encode(self.my_key.sign(content.encode("ascii"))).decode("utf-8")
        }

        if not nearest_nodes:
            self.data[hashed_key] = value

        for node in nearest_nodes:
            node.store(hashed_key, value, socket=self.server.socket, peer_id=self.peer.id)
