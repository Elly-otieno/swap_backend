import os
import json
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

def deploy_contracts():
    load_dotenv()

    rpc_url = os.getenv('BLOCKCHAIN_RPC_URL', 'https://sepolia.base.org')
    private_key = os.getenv('BLOCKCHAIN_PRIVATE_KEY')

    if not private_key:
        print("Error: BLOCKCHAIN_PRIVATE_KEY not found in .env")
        return

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("Error: Could not connect to blockchain")
        return

    account = Account.from_key(private_key)
    print(f"Deploying from: {account.address}")

    balance = w3.eth.get_balance(account.address)
    print(f"Balance: {w3.from_wei(balance, 'ether')} ETH")

    if balance == 0:
        print("Error: Insufficient balance for deployment")
        return

    contracts_to_deploy = ['UserRegistry', 'SIMSwapManager', 'AccessControl']
    deployed_addresses = {}

    abi_dir = 'blockchain/abis'

    for name in contracts_to_deploy:
        print(f"\nDeploying {name}...")

        abi_path = os.path.join(abi_dir, f"{name}.json")
        bytecode_path = os.path.join(abi_dir, f"{name}_bytecode.txt")

        with open(abi_path, 'r') as f:
            abi = json.load(f)
        with open(bytecode_path, 'r') as f:
            bytecode = f.read().strip()

        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        nonce = w3.eth.get_transaction_count(account.address)

        # Build transaction
        tx = contract.constructor().build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price
        })

        # Sign and send
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"Transaction sent: {w3.to_hex(tx_hash)}")
        print("Waiting for confirmation...")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        address = receipt.contractAddress
        deployed_addresses[name] = address
        print(f"{name} deployed to: {address}")

    print("\n--- DEPLOYMENT SUCCESSFUL ---")
    print("Update your .env file with these addresses:")
    print(f"CONTRACT_USER_REGISTRY={deployed_addresses['UserRegistry']}")
    print(f"CONTRACT_SIM_SWAP_MANAGER={deployed_addresses['SIMSwapManager']}")
    print(f"CONTRACT_ACCESS_CONTROL={deployed_addresses['AccessControl']}")

if __name__ == "__main__":
    deploy_contracts()
