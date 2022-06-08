import os
import time
import copy
import logging
from pathlib import Path


from django.apps import AppConfig

from blockchain_app.utilities.connectivity import connect_to_blockchain
from django.conf import settings

from threading import Thread


logger = logging.getLogger(__name__)


def send_event():
    while True:

        # Clock
        time.sleep(5.0)
        settings.PERIODIC_SIGNAL.send("app")

        # Get a copy
        to_db = copy.deepcopy(settings.TRADE_DB_OBJECTS_BUFFER)

        # Reset buffer
        settings.TRADE_DB_OBJECTS_BUFFER = {}

        # Write to our database
        from trade_listener_app.models import TradeData
        for user_id, trades in to_db.items():

            # Write to DB
            TradeData.objects.bulk_create(trades, ignore_conflicts=True)

            # Account for this user
            user_blockchain_account = settings.BLOCKCHAIN_ACCOUNT_USERS[user_id]
            settings.BLOCKCHAIN_W3.eth.default_account = user_blockchain_account

            # Write to the blockchain
            # write_hashes_to_blockchain(settings.BLOCKCHAIN_W3, user_id, trades)

            # Make a call to the blockchain via this instance (test)
            ts_block = settings.BLOCKCHAIN_CONTRACT_INSTANCE.functions.currentBlockTime().call()
            print(ts_block)

def print_something(*args, **kwargs):
    print(f"The length of the buffer is: {len(settings.TRADE_DB_OBJECTS_BUFFER)}")



class BlockchainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blockchain_app'

    def ready(self):
        print(f"App Blockchain starting...")
        w3 = connect_to_blockchain()

        if not w3.isConnected():
            raise ConnectionError("Blockchain connection unavailable.")

        # Displays
        logger.info(f"Blockchain connection established.")
        settings.BLOCKCHAIN_W3 = w3

        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        this_dir = Path(__file__).resolve().parent

        from blockchain_app.utilities.compile import maybe_install_compiler
        contracts_path = f"{this_dir}/contracts/"
        maybe_install_compiler(contracts_path)

        main_smart_contract_path = f"{contracts_path}PerformanceTracker.sol"
        from blockchain_app.utilities.compile import get_abi_bytecode
        abi, bytecode = get_abi_bytecode(main_smart_contract_path)

        # Store for later
        settings.BLOCKCHAIN_ABI = abi
        settings.BLOCKCHAIN_BYTECODE = bytecode

        # Users will be 0 or 1, not 9.
        platform_account = w3.eth.accounts[9]
        w3.eth.default_account = platform_account
        settings.BLOCKCHAIN_ACCOUNT_UI = platform_account

        # Smart contract representation in Python
        PerformanceTracker = w3.eth.contract(abi=abi, bytecode=bytecode)

        # Deploy
        tx_hash = PerformanceTracker.constructor().transact()
        print(f"The transaction hash for smart contract deployment: {tx_hash.hex()}")

        # Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        print(f"The contract was deployed on address {contract_address}")
        settings.BLOCKCHAIN_CONTRACT_INSTANCE = contract_address

        # Instantiate the contract locally
        performanceTrackerInstance = w3.eth.contract(address=contract_address, abi=abi)
        settings.BLOCKCHAIN_CONTRACT_INSTANCE = performanceTrackerInstance

        # Populate some fake accounts
        for i in range(5):
            print(f"Registering user {i}.")
            settings.BLOCKCHAIN_ACCOUNT_USERS[i] = w3.eth.accounts[i]
            #TODO Call registerUser(...)



        settings.PERIODIC_SIGNAL.connect(print_something)

        new_thread = Thread(target=send_event)
        new_thread.start()
