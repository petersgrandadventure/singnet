import json
import logging
import socketserver

import nacl.encoding
import nacl.signing

from .peer import Peer

logger = logging.getLogger(__name__)


class DHTRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            message = json.loads(self.request[0].decode("utf-8").strip())
            message_type = message["message_type"]

            logger.debug('Handling message type" %s', message_type)

            if message_type == "ping":
                self.handle_ping(message)
            elif message_type == "pong":
                self.handle_pong(message)
            elif message_type == "find_node":
                self.handle_find(message)
            elif message_type == "find_value":
                self.handle_find(message, find_value=True)
            elif message_type == "found_nodes":
                self.handle_found_nodes(message)
            elif message_type == "found_value":
                self.handle_found_value(message)
            elif message_type == "store":
                self.handle_store(message)
            elif message_type == "push":
                self.handle_push(message)
        except:
            return

        client_host, client_port = self.client_address
        peer_id = message["peer_id"]
        new_peer = Peer(client_host, client_port, peer_id)
        self.server.dht.buckets.insert(new_peer)

    def handle_ping(self, message):
        client_host, client_port = self.client_address
        id = message["peer_id"]
        peer = Peer(client_host, client_port, id)
        peer.pong(socket=self.server.socket, peer_id=self.server.dht.peer.id, lock=self.server.send_lock)

    def handle_pong(self, message):
        pass

    def handle_find(self, message, find_value=False):
        key = message["id"]
        id = message["peer_id"]
        client_host, client_port = self.client_address
        peer = Peer(client_host, client_port, id)
        response_socket = self.request[1]
        if find_value and (key in self.server.dht.data):
            value = self.server.dht.data[key]
            peer.found_value(id, value, message["rpc_id"], socket=response_socket, peer_id=self.server.dht.peer.id, lock=self.server.send_lock)
        else:
            nearest_nodes = self.server.dht.buckets.nearest_nodes(id)
            if not nearest_nodes:
                nearest_nodes.append(self.server.dht.peer)
            nearest_nodes = [nearest_peer.astriple() for nearest_peer in nearest_nodes]
            peer.found_nodes(id, nearest_nodes, message["rpc_id"], socket=response_socket, peer_id=self.server.dht.peer.id, lock=self.server.send_lock)

    def handle_found_nodes(self, message):
        rpc_id = message["rpc_id"]
        shortlist = self.server.dht.rpc_ids[rpc_id]
        del self.server.dht.rpc_ids[rpc_id]
        nearest_nodes = [Peer(*peer) for peer in message["nearest_nodes"]]
        shortlist.update(nearest_nodes)

    def handle_found_value(self, message):
        rpc_id = message["rpc_id"]
        shortlist = self.server.dht.rpc_ids[rpc_id]
        del self.server.dht.rpc_ids[rpc_id]
        shortlist.set_complete(message["value"])

    def handle_store(self, message):
        key = message["id"]

        # Verify updated message is signed with same key.
        if key in self.server.dht.data:
            # Signature is valid.
            # (Raises exception if not.)
            ret = nacl.signing.VerifyKey(self.server.dht.data[key]["key"], encoder=nacl.encoding.Base64Encoder).verify(nacl.encoding.Base64Encoder.decode(message["value"]["signature"]))
            if type(ret) == bytes:
                ret = ret.decode("utf-8")

            # Check that the signature corresponds to this message.
            message_content = message["value"]["content"]
            if ret != message_content:
                return

        self.server.dht.data[key] = message["value"]

    def handle_push(self, message):
        pass
