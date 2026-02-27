import os
import json
import logging
import hashlib
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from web3 import Web3
from eth_account import Account
from blockchain.models import Block, BlockchainTransaction

logger = logging.getLogger(__name__)

class BlockchainService:
    def __init__(self):
        self.enabled = os.getenv('ENABLE_BLOCKCHAIN', 'false').lower() == 'true'
        if not self.enabled:
            logger.info("Blockchain integration is disabled.")
            return

        self.rpc_url = os.getenv('BLOCKCHAIN_RPC_URL', 'https://sepolia.base.org')
        self.private_key = os.getenv('BLOCKCHAIN_PRIVATE_KEY')
        self.chain_id = int(os.getenv('BLOCKCHAIN_CHAIN_ID', '84532'))

        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if self.private_key:
            self.account = Account.from_key(self.private_key)
            logger.info(f"Blockchain wallet initialized: {self.account.address}")
        else:
            self.account = None
            logger.warning("No private key provided, blockchain writes will not be available")

        # Load contract ABIs and addresses
        self.contract_addresses = {
            'userRegistry': os.getenv('CONTRACT_USER_REGISTRY'),
            'simSwapManager': os.getenv('CONTRACT_SIM_SWAP_MANAGER'),
            'accessControl': os.getenv('CONTRACT_ACCESS_CONTROL')
        }

        self.contracts = {}
        try:
            abi_dir = os.path.join(os.path.dirname(__file__), 'abis')
            for name, address in self.contract_addresses.items():
                if address:
                    abi_path = os.path.join(abi_dir, f"{self._to_camel_case(name)}.json")
                    if os.path.exists(abi_path):
                        with open(abi_path, 'r') as f:
                            abi = json.load(f)
                        self.contracts[name] = self.w3.eth.contract(address=address, abi=abi)
            logger.info("Blockchain contracts initialized")
        except Exception as e:
            logger.error(f"Failed to initialize blockchain contracts: {e}")

    def _to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)

    def _get_nonce(self):
        return self.w3.eth.get_transaction_count(self.account.address)

    def _send_transaction(self, contract_func, *args, **kwargs):
        if not self.enabled or not self.account:
            return None

        try:
            nonce = self._get_nonce()
            gas_price = self.w3.eth.gas_price

            # Build transaction
            tx = contract_func(*args).build_transaction({
                'chainId': self.chain_id,
                'gas': 500000,
                'gasPrice': gas_price,
                'nonce': nonce,
            })

            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            logger.error(f"Blockchain transaction failed: {e}")
            return None

    def register_user(self, user_id, phone_number, biometric_hash, id_number):
        """Register user identity on blockchain"""
        if not self.enabled:
            return {"status": "mocked", "txHash": "0x" + "0"*64}

        phone_hash = self.w3.keccak(text=phone_number)
        # Simplified identity hash for demo
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
        """Initiate SIM swap on blockchain"""
        if not self.enabled or 'simSwapManager' not in self.contracts:
            # Create a mock transaction in database for demonstration if needed
            tx_hash = "0x" + hashlib.sha256(f"initiate_{request_id}".encode()).hexdigest()
            BlockchainTransaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    'contract_address': self.contract_addresses.get('simSwapManager') or "0x0000000000000000000000000000000000000002",
                    'function_name': 'initiateSIMSwap',
                    'user_id': user_id,
                    'request_id': request_id,
                    'status': 'CONFIRMED', # Mocked as confirmed
                    'block_number': 12345
                }
            )
            return {"status": "mocked", "txHash": tx_hash}

        phone_hash = self.w3.keccak(text=phone_number)
        old_sim_hash = self.w3.keccak(text=old_sim_serial) if old_sim_serial else b'\x00'*32
        new_sim_hash = self.w3.keccak(text=new_sim_serial)

        tx_hash = self._send_transaction(
            self.contracts['simSwapManager'].functions.initiateSIMSwap,
            phone_hash,
            old_sim_hash,
            new_sim_hash
        )

        if tx_hash:
            BlockchainTransaction.objects.create(
                tx_hash=tx_hash,
                contract_address=self.contract_addresses['simSwapManager'],
                function_name='initiateSIMSwap',
                user_id=user_id,
                request_id=request_id,
                status='PENDING'
            )

        return {"txHash": tx_hash}

    def record_verification(self, request_id, verification_type):
        """Record verification completion on blockchain"""
        if not self.enabled or 'simSwapManager' not in self.contracts:
            tx_hash = "0x" + hashlib.sha256(f"verify_{request_id}_{verification_type}".encode()).hexdigest()
            BlockchainTransaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    'contract_address': self.contract_addresses.get('simSwapManager') or "0x0000000000000000000000000000000000000002",
                    'function_name': 'completeVerification',
                    'request_id': request_id,
                    'status': 'CONFIRMED',
                    'block_number': 12346
                }
            )
            return {"status": "mocked", "txHash": tx_hash}

        # Verification type mapping
        type_map = {
            'PERSONAL_DETAILS': 0,
            'BIOMETRIC': 1,
            'ID_DOCUMENT': 2,
            'SECURITY_QUESTIONS': 3,
            'BIOMETRIC_AND_ID': 4
        }
        type_enum = type_map.get(verification_type, 0)

        # We use a hash of request_id as swapId for simplicity if it's bytes32 in contract
        swap_id = self.w3.keccak(text=request_id)

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

    def approve_sim_swap(self, request_id):
        """Approve SIM swap on blockchain"""
        if not self.enabled or 'simSwapManager' not in self.contracts:
            tx_hash = "0x" + hashlib.sha256(f"approve_{request_id}".encode()).hexdigest()
            BlockchainTransaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    'contract_address': self.contract_addresses.get('simSwapManager') or "0x0000000000000000000000000000000000000002",
                    'function_name': 'approveSIMSwap',
                    'request_id': request_id,
                    'status': 'CONFIRMED',
                    'block_number': 12347
                }
            )
            return {"status": "mocked", "txHash": tx_hash}

        swap_id = self.w3.keccak(text=request_id)

        tx_hash = self._send_transaction(
            self.contracts['simSwapManager'].functions.approveSIMSwap,
            swap_id
        )

        if tx_hash:
            BlockchainTransaction.objects.create(
                tx_hash=tx_hash,
                contract_address=self.contract_addresses['simSwapManager'],
                function_name='approveSIMSwap',
                request_id=request_id,
                status='PENDING'
            )

        return {"txHash": tx_hash}

    def log_event(self, event, msisdn):
        """Legacy support for existing log_event calls"""
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

        # Also try to record on real blockchain if it's a major event
        if event == "SWAP_COMPLETED":
            # Find a recent request for this msisdn
            from swap.models import SwapSession
            session = SwapSession.objects.filter(line__msisdn=msisdn).order_by('-created_at').first()
            if session:
                self.approve_sim_swap(str(session.id))

blockchain_service = BlockchainService()

def log_event(event, msisdn):
    blockchain_service.log_event(event, msisdn)
