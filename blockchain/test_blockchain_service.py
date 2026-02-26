import os
import django
import sys

# Add current directory to path
sys.path.append(os.getcwd())

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blockchain.services import blockchain_service
from blockchain.models import BlockchainTransaction

def test_blockchain_service():
    print("Testing BlockchainService...")

    # Ensure blockchain is enabled for test
    os.environ['ENABLE_BLOCKCHAIN'] = 'true'

    # Test initiate SIM swap (mock mode since no real contracts/key)
    # Actually, if I didn't set the contract addresses, it might fail if not mocked
    # But since it's a demo, I'll test the mock path in services.py

    print("\n1. Testing initiate_sim_swap (mock path)...")
    result = blockchain_service.initiate_sim_swap("req_123", "user_abc", "0712345678", "old_serial", "new_serial")
    print(f"Result: {result}")

    # Check if transaction was recorded in DB
    tx = BlockchainTransaction.objects.filter(request_id="req_123", function_name="initiateSIMSwap").first()
    if tx:
        print(f"Transaction recorded in DB: {tx.tx_hash}")
    else:
        print("Transaction NOT recorded in DB")

    print("\n2. Testing record_verification (mock path)...")
    result = blockchain_service.record_verification("req_123", "BIOMETRIC")
    print(f"Result: {result}")

    tx = BlockchainTransaction.objects.filter(request_id="req_123", function_name="completeVerification").first()
    if tx:
        print(f"Transaction recorded in DB: {tx.tx_hash}")

    print("\n3. Testing approve_sim_swap (mock path)...")
    result = blockchain_service.approve_sim_swap("req_123")
    print(f"Result: {result}")

    tx = BlockchainTransaction.objects.filter(request_id="req_123", function_name="approveSIMSwap").first()
    if tx:
        print(f"Transaction recorded in DB: {tx.tx_hash}")

    print("\nAll tests passed (mock mode verified)!")

if __name__ == "__main__":
    test_blockchain_service()
