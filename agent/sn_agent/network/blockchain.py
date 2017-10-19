import Web3 as Web3
from web3 import HTTPProvider

from sn_agent import ontology


class BlockChain:
    def __init__(self, client_url) -> None:
        self.conn = Web3(HTTPProvider(client_url))

    def get_agents_for_ontology(self, ontology_id):

        # Total short circuit here - this needs to go out to the blockchain
        if ontology.DOCUMENT_SUMMARIZER_ID:
            # Send the top part to Alice
            return ['b545478a-971a-48ec-bc56-4b9b7176799c', ]
        else:
            # Everything else goes to Bob
            return ['c545478a-971a-48ec-bc56-aaaaaaaaaaaa']
