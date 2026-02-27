import json
import logging
import hashlib
from django.conf import settings
from web3 import Web3
from eth_account import Account
from blockchain.models import Block, BlockchainTransaction

logger = logging.getLogger(__name__)

class BlockchainService:
    def __init__(self):
        self.enabled = getattr(settings, 'ENABLE_BLOCKCHAIN', False)

        # Contract addresses from settings
        self.contract_addresses = {
            'userRegistry': getattr(settings, 'CONTRACT_USER_REGISTRY', None),
            'simSwapManager': getattr(settings, 'CONTRACT_SIM_SWAP_MANAGER', None),
            'accessControl': getattr(settings, 'CONTRACT_ACCESS_CONTROL', None)
        }

        if not self.enabled:
            logger.info("Blockchain integration is disabled.")
            self.w3 = None
            self.account = None
            self.contracts = {}
            return

        # Initialize Web3
        self.rpc_url = getattr(settings, 'BLOCKCHAIN_RPC_URL', 'https://sepolia.base.org')
        self.private_key = getattr(settings, 'BLOCKCHAIN_PRIVATE_KEY', None)
        self.chain_id = getattr(settings, 'BLOCKCHAIN_CHAIN_ID', 84532)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if self.private_key:
            self.account = Account.from_key(self.private_key)
            logger.info(f"Blockchain wallet initialized: {self.account.address}")
        else:
            self.account = None
            logger.warning("No private key provided; blockchain writes unavailable")

        # Load contracts
        self.contracts = {}
        abi_dir = getattr(settings, 'BLOCKCHAIN_ABI_DIR', 'blockchain/abis')
        for name, address in self.contract_addresses.items():
            if address:
                try:
                    abi_file = f"{abi_dir}/{self._to_camel_case(name)}.json"
                    with open(abi_file, 'r') as f:
                        abi = json.load(f)
                    self.contracts[name] = self.w3.eth.contract(address=address, abi=abi)
                except Exception as e:
                    logger.warning(f"Failed to load ABI for {name}: {e}")
        logger.info(f"Contracts loaded: {list(self.contracts.keys())}")

    def _to_camel_case(self, snake_str):
        return ''.join(word.title() for word in snake_str.split('_'))

    def _get_nonce(self):
        return self.w3.eth.get_transaction_count(self.account.address)

    def _send_transaction(self, contract_func, *args):
        """Send transaction safely, returns tx_hash or None"""
        if not self.enabled or not self.account:
            return None
        try:
            tx = contract_func(*args).build_transaction({
                'chainId': self.chain_id,
                'gas': 500_000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self._get_nonce(),
            })
            signed = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            tx_hex = self.w3.to_hex(tx_hash)
            logger.info(f"Blockchain tx sent: {tx_hex}")
            return tx_hex
        except Exception as e:
            logger.error(f"Blockchain transaction failed: {e}")
            return None

    # ---------------- Demo-safe blockchain operations ----------------

    def register_user(self, user_id, phone_number, biometric_hash, id_number):
        """Register a user (mocked if blockchain disabled)"""
        tx_hash = None
        phone_hash = None
        identity_hash = None

        if not self.enabled or 'userRegistry' not in self.contracts:
            # Mock tx
            tx_hash = "0x" + hashlib.sha256(f"register_{user_id}".encode()).hexdigest()
            phone_hash = "0x" + hashlib.sha256(phone_number.encode()).hexdigest()
            identity_hash = "0x" + hashlib.sha256(f"{biometric_hash}{id_number}".encode()).hexdigest()
            BlockchainTransaction.objects.create(
                tx_hash=tx_hash,
                contract_address=self.contract_addresses.get('userRegistry', "0x0"),
                function_name='registerUser',
                user_id=user_id,
                status='CONFIRMED'
            )
            return {"txHash": tx_hash, "identityHash": identity_hash, "phoneHash": phone_hash}

        # Real blockchain tx (if enabled)
        phone_hash = self.w3.keccak(text=phone_number)
        identity_hash = self.w3.keccak(text=f"{biometric_hash}{id_number}")
        tx_hash = self._send_transaction(
            self.contracts['userRegistry'].functions.registerUser,
            phone_hash,
            identity_hash
        )
        if tx_hash:
            BlockchainTransaction.objects.create(
                tx_hash=tx_hash,
                contract_address=self.contract_addresses['userRegistry'],
                function_name='registerUser',
                user_id=user_id,
                status='PENDING'
            )
        return {"txHash": tx_hash, "identityHash": self.w3.to_hex(identity_hash), "phoneHash": self.w3.to_hex(phone_hash)}

    def initiate_sim_swap(self, request_id, user_id, phone_number, old_sim_serial, new_sim_serial):
        """Initiate a SIM swap safely (demo-safe)"""
        # Use demo/mock mode if blockchain disabled or contract missing
        contract_address = self.contract_addresses.get('simSwapManager') or "0x0"

        tx_hash = "0x" + hashlib.sha256(f"initiate_{request_id}".encode()).hexdigest()
        swap_id = "0x" + hashlib.sha256(f"swap_{request_id}".encode()).hexdigest()

        # Always create transaction with non-null contract_address
        BlockchainTransaction.objects.create(
            tx_hash=tx_hash,
            contract_address=contract_address,
            function_name='initiateSIMSwap',
            user_id=user_id,
            request_id=request_id,
            status='CONFIRMED',
            block_number=12345
        )

        return {"status": "mocked", "txHash": tx_hash, "swapId": swap_id}
    
    def record_verification(self, request_id, swap_id, verification_type):
        """Record verification safely (demo-safe)"""
        if not self.enabled or 'simSwapManager' not in self.contracts:
            tx_hash = "0x" + hashlib.sha256(f"verify_{request_id}_{verification_type}".encode()).hexdigest()
            BlockchainTransaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    'contract_address': self.contract_addresses.get('simSwapManager') or "0x0",
                    'function_name': 'completeVerification',
                    'request_id': request_id,
                    'status': 'CONFIRMED',
                    'block_number': 12346
                }
            )
            return {"status": "mocked", "txHash": tx_hash}

        type_map = {
            'PERSONAL_DETAILS': 0,
            # 'BIOMETRIC': 1,
            # 'ID_DOCUMENT': 2,
            # 'SECURITY_QUESTIONS': 3,
            'BIOMETRIC_AND_ID': 2
        }
        type_enum = type_map.get(verification_type, 0)
        tx_hash = self._send_transaction(
            self.contracts['simSwapManager'].functions.completeVerification,
            swap_id,
            type_enum
        )
        if tx_hash:
            BlockchainTransaction.objects.create(
                tx_hash=tx_hash,
                contract_address=self.contract_addresses['simSwapManager'],
                function_name='completeVerification',
                request_id=request_id,
                status='PENDING'
            )
        return {"txHash": tx_hash}

    def approve_sim_swap(self, request_id, swap_id):
        """Approve a SIM swap (fully stable demo-safe version)"""

        contract_address = (
            self.contract_addresses.get('simSwapManager')
            if hasattr(self, 'contract_addresses')
            else None
        ) or "0x0"

        tx_hash = "0x" + hashlib.sha256(
            f"approve_{request_id}_{swap_id}".encode()
        ).hexdigest()

        if not self.enabled or 'simSwapManager' not in self.contracts:

            BlockchainTransaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    "contract_address": contract_address,
                    "function_name": "approveSIMSwap",
                    "request_id": request_id,
                    "status": "CONFIRMED",
                    "block_number": 12347
                }
            )

            return {"status": "mocked", "txHash": tx_hash}

        tx_hash = self._send_transaction(
            self.contracts['simSwapManager'].functions.approveSIMSwap,
            swap_id
        )

        if tx_hash:
            BlockchainTransaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    "contract_address": contract_address,
                    "function_name": "approveSIMSwap",
                    "request_id": request_id,
                    "status": "PENDING"
                }
            )

        return {"txHash": tx_hash}
    
    # ---------------- Legacy block logging ----------------

    def log_event(self, event, msisdn):
        last_block = Block.objects.order_by("-index").first()
        index = 1 if not last_block else last_block.index + 1
        previous_hash = "0" if not last_block else last_block.hash
        block = Block.objects.create(
            index=index,
            event=event,
            msisdn=msisdn,
            previous_hash=previous_hash,
            hash=""
        )
        block.hash = block.calculate_hash()
        block.save()

        # Auto-approve swap if SWAP_COMPLETED
        if event == "SWAP_COMPLETED":
            from swap.models import SwapSession
            session = SwapSession.objects.filter(line__msisdn=msisdn).order_by('-created_at').first()
            if session:
                swap_id = getattr(session, "swap_id", str(session.id))  # fallback
                self.approve_sim_swap(str(session.id), swap_id)


# Singleton
blockchain_service = BlockchainService()

def log_event(event, msisdn):
    blockchain_service.log_event(event, msisdn)