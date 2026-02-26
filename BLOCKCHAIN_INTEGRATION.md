# SwapSecure Blockchain Integration

This document describes the blockchain integration for the SwapSecure project, ported from Repository #2 to Repository #1.

## Overview

The blockchain integration provides an immutable audit trail for all SIM swap transactions. Every major step in the SIM swap process is recorded on the Base Sepolia testnet using smart contracts.

## Architecture

- **Blockchain Network**: Base Sepolia
- **Smart Contracts**:
  - `UserRegistry`: Stores user identity hashes.
  - `SIMSwapManager`: Manages the lifecycle of a SIM swap request.
  - `AccessControl`: Manages permissions for system actors.
- **Service Layer**: `blockchain/services.py` provides the Python interface to the blockchain using `web3.py`.

## Configuration

The integration is controlled by environment variables in the `.env` file.

### Environment Variables

```bash
# Feature Flag
ENABLE_BLOCKCHAIN=true

# Blockchain Connection
BLOCKCHAIN_NETWORK=base-sepolia
BLOCKCHAIN_RPC_URL=https://sepolia.base.org
BLOCKCHAIN_PRIVATE_KEY=0x...
BLOCKCHAIN_CHAIN_ID=84532

# Smart Contract Addresses
CONTRACT_USER_REGISTRY=0x...
CONTRACT_SIM_SWAP_MANAGER=0x...
CONTRACT_ACCESS_CONTROL=0x...
```

## Integration Points

1. **SIM Swap Initiation**: When `StartSwapView` is called, a new swap is initiated on the blockchain.
2. **Verification Steps**: Each vetting step (Primary, Secondary, Face, ID, Didit) records its completion on the blockchain.
3. **SIM Swap Approval**: When `CompleteSwapView` is called, the swap is marked as approved on the blockchain.

## Demonstration Endpoints

The following endpoints are available for demonstrating the blockchain audit trail:

- `GET /api/v1/blockchain/actors/`: Defined problem and actors.
- `GET /api/v1/blockchain/architecture/`: System architecture details.
- `GET /api/v1/blockchain/record-flow/`: Step-by-step record flow documentation.
- `GET /api/v1/blockchain/mock-external-apis/`: Information about mocked external APIs.
- `GET /api/v1/blockchain/demo-transaction/`: A complete transaction flow example.
- `GET /api/v1/blockchain/ledger-state/<request_id>/`: Before/after ledger state for a request.
- `GET /api/v1/blockchain/transactions/`: Immutable transaction list with hash chain.
- `GET /api/v1/blockchain/audit-trail/<user_id>/`: Complete audit trail for a user.

## Smart Contract Compilation

To recompile the smart contracts and regenerate ABIs, run:

```bash
python blockchain/compile_contracts.py
```

The ABIs will be generated in `blockchain/abis/`.

## Mock Mode

If `ENABLE_BLOCKCHAIN` is set to `false` or if contract addresses/private keys are missing, the service will operate in **Mock Mode**, generating simulated transaction hashes and recording them in the local database for demonstration purposes.
