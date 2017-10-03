import logging
import miniupnpc
import socketserver
import threading

logger = logging.getLogger(__name__)


class DHTServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, host_address, handler_cls):

        logger.debug("Starting DHT Sever on %s", host_address)

        socketserver.UDPServer.__init__(self, host_address, handler_cls)
        self.send_lock = threading.Lock()

    def try_upnp_portmap(self, port):

        upnp = miniupnpc.UPnP()
        upnp.discover()

        try:
            upnp.selectigd()
            result = upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 'SN Agent dht port: %u' % port, '', )
            logger.debug('UPnP result: %s', result)
        except:
            logging.error("Unable to port map using UPnP")
