import logging
from web3 import Web3

from blockchain_app.utilities.common import LOCAL_BLOCKCHAIN

logger = logging.getLogger(__name__)


def connect_to_blockchain(address=LOCAL_BLOCKCHAIN):
    # Connect to the blockchain_app running on Truffle
    w3 = Web3(Web3.HTTPProvider(address))
    if not test_connection(w3):
        logger.warning("Blockchain connection unavailable.")
    return w3


def test_connection(w3):
    try:
        is_conn = w3.isConnected()
        return is_conn
    except:
        return False
