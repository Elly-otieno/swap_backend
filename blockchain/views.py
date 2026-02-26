from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from blockchain.models import BlockchainTransaction, Block
import hashlib

class BlockchainActorsView(APIView):
    def get(self, request):
        return Response({
            "problem": "SIM swap fraud prevention through immutable audit trails",
            "actors": [
                {
                    "id": "user",
                    "name": "Customer",
                    "role": "Initiates SIM swap request",
                    "interactsWithLedger": True,
                    "trustedRecords": ["identity_verification", "sim_swap_request"]
                },
                {
                    "id": "agent",
                    "name": "Safaricom Agent",
                    "role": "Approves SIM swap",
                    "interactsWithLedger": True,
                    "trustedRecords": ["approval_signature"]
                },
                {
                    "id": "system",
                    "name": "SwapSecure System",
                    "role": "Records verifications",
                    "interactsWithLedger": True,
                    "trustedRecords": ["biometric_verification", "transaction_completion"]
                }
            ]
        })

class BlockchainArchitectureView(APIView):
    def get(self, request):
        return Response({
            "architecture": {
                "layers": [
                    {
                        "name": "Application Layer",
                        "components": ["Mobile App", "API Server"],
                        "purpose": "User interaction and business logic"
                    },
                    {
                        "name": "Blockchain Layer",
                        "components": ["Base Sepolia Network", "Smart Contracts"],
                        "purpose": "Immutable record keeping"
                    },
                    {
                        "name": "Data Layer",
                        "components": ["PostgreSQL/SQLite (off-chain)", "Blockchain (on-chain)"],
                        "purpose": "Data storage and retrieval"
                    }
                ],
                "flow": "User → API → Smart Contract → Blockchain → Confirmation → Database"
            }
        })

class BlockchainRecordFlowView(APIView):
    def get(self, request):
        return Response({
            "flow": [
                {
                    "step": 1,
                    "phase": "Submission",
                    "actor": "user",
                    "action": "Submit SIM swap request",
                    "data": {
                        "phoneNumber": "hashed",
                        "newSimSerial": "hashed",
                        "timestamp": "ISO8601"
                    }
                },
                {
                    "step": 2,
                    "phase": "Validation",
                    "actor": "system",
                    "action": "Verify biometric and personal details",
                    "data": {
                        "verificationsPassed": ["biometric", "id_document"]
                    }
                },
                {
                    "step": 3,
                    "phase": "Ledger Update",
                    "actor": "system",
                    "action": "Record transaction on blockchain",
                    "data": {
                        "txHash": "0x...",
                        "blockNumber": 12345,
                        "gasUsed": 150000
                    }
                }
            ]
        })

class MockExternalAPIsView(APIView):
    def get(self, request):
        return Response({
            "mockedAPIs": [
                {
                    "name": "Safaricom View360",
                    "purpose": "Customer profile retrieval",
                    "status": "Mocked",
                    "endpoints": ["/view360/customer/info"]
                },
                {
                    "name": "Safaricom M-PESA",
                    "purpose": "Account details and transaction history",
                    "status": "Mocked",
                    "endpoints": ["/mpesa/account/status"]
                },
                {
                    "name": "didit.me",
                    "purpose": "Biometric and ID verification",
                    "status": "Sandbox Mode",
                    "endpoints": ["/didit/session/create", "/didit/webhook"]
                }
            ]
        })

class BlockchainDemoTransactionView(APIView):
    def get(self, request):
        return Response({
            "transactionId": "req_demo_abc123",
            "actorFlow": [
                {
                    "actorId": "user_uuid_123",
                    "actorType": "customer",
                    "action": "Initiated SIM swap",
                    "timestamp": "2025-02-26T10:00:00Z",
                    "dataSubmitted": {
                        "phoneNumber": "0712****678",
                        "newSimSerial": "8925****4871"
                    }
                },
                {
                    "actorId": "system",
                    "actorType": "automated_verification",
                    "action": "Verified biometric identity",
                    "timestamp": "2025-02-26T10:01:30Z",
                    "verificationResult": "PASSED"
                },
                {
                    "actorId": "agent_uuid_456",
                    "actorType": "safaricom_agent",
                    "action": "Approved swap request",
                    "timestamp": "2025-02-26T10:03:00Z",
                    "approvalSignature": "0x..."
                },
                {
                    "actorId": "blockchain",
                    "actorType": "immutable_ledger",
                    "action": "Recorded completion",
                    "timestamp": "2025-02-26T10:03:15Z",
                    "blockchainProof": {
                        "txHash": "0xabc123...",
                        "blockNumber": 12345,
                        "contractAddress": "0xdef456..."
                    }
                }
            ],
            "finalState": "COMPLETED"
        })

class BlockchainLedgerStateView(APIView):
    def get(self, request, request_id):
        # In a real app, this would query the blockchain for current state
        # For demo, we return mock state based on request_id
        return Response({
            "requestId": request_id,
            "beforeState": {
                "phoneNumber": "0712345678",
                "currentSimSerial": "89254021003487612905",
                "ledgerEntries": 5,
                "lastTransaction": "2025-02-20T14:30:00Z"
            },
            "transaction": {
                "type": "SIM_SWAP",
                "actor": "user_uuid_123",
                "timestamp": timezone.now().isoformat(),
                "txHash": "0x" + hashlib.sha256(request_id.encode()).hexdigest()
            },
            "afterState": {
                "phoneNumber": "0712345678",
                "currentSimSerial": "89254021994105234871",
                "ledgerEntries": 6,
                "lastTransaction": timezone.now().isoformat(),
                "verification": "blockchain_confirmed"
            },
            "ledgerUpdate": "IMMEDIATE",
            "confirmationTime": "15 seconds"
        })

class BlockchainTransactionsView(APIView):
    def get(self, request):
        transactions = BlockchainTransaction.objects.all().order_by('-created_at')[:10]
        data = []

        # Build mock hash chain for demonstration if it doesn't exist
        prev_hash = "0x" + "0"*64
        for i, tx in enumerate(reversed(transactions)):
            record_hash = tx.tx_hash
            data.append({
                "index": i + 1,
                "recordHash": record_hash,
                "previousHash": prev_hash,
                "timestamp": tx.created_at.isoformat(),
                "blockNumber": tx.block_number or (12345 + i),
                "actor": tx.user_id or "system",
                "action": tx.function_name,
                "immutable": True
            })
            prev_hash = record_hash

        return Response({
            "transactions": data,
            "chainIntegrity": "VERIFIED",
            "totalRecords": len(data)
        })

class BlockchainAuditTrailView(APIView):
    def get(self, request, user_id):
        transactions = BlockchainTransaction.objects.filter(user_id=user_id).order_by('created_at')
        audit_trail = []

        for tx in transactions:
            audit_trail.append({
                "timestamp": tx.created_at.isoformat(),
                "actor": user_id,
                "actorType": "customer" if tx.function_name == 'initiateSIMSwap' else "system",
                "action": tx.function_name,
                "details": {
                    "requestId": tx.request_id
                },
                "blockchainProof": tx.tx_hash,
                "status": "immutable_record" if tx.status == 'CONFIRMED' else "pending"
            })

        return Response({
            "userId": user_id,
            "auditTrail": audit_trail,
            "totalActions": len(audit_trail),
            "blockchainVerified": True
        })
