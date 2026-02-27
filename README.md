# Swap Secure: Blockchain Backend (Django)

This is the core API for the Swap Secure ecosystem. It manages user sessions, validates phone numbers via the database, and interfaces with the **Base Sepolia** blockchain to record immutable verification logs.



##  Quick Start

### 1. Prerequisites
* **Python 3.11+**
* **PostgreSQL** (Local or [Neon.tech](https://neon.tech))
* **Base Sepolia RPC URL** (via Alchemy, Infura, or public nodes)

### 2. Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
```bash
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:pass@localhost:5432/dbname

# Blockchain Configuration
ENABLE_BLOCKCHAIN=true
BLOCKCHAIN_RPC_URL=[https://sepolia.base.org](https://sepolia.base.org)
BLOCKCHAIN_PRIVATE_KEY=0x...
BLOCKCHAIN_CHAIN_ID=84532

# Smart Contract Addresses
CONTRACT_USER_REGISTRY=0x...
CONTRACT_SIM_SWAP_MANAGER=0x...
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser  # To access Django Admin
python manage.py runserver
```

### 5. Blockchain Integration
This project includes blockchain integration (Base Sepolia) for SIM swap verification.
See [BLOCKCHAIN_INTEGRATION.md](BLOCKCHAIN_INTEGRATION.md) for details.

## Security
- Hashing: Phone numbers and IDs are hashed using keccak256 before being sent to the blockchain.
- Nonces: Sequential transaction management for EVM compatibility.
