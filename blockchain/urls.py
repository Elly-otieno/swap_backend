from django.urls import path
from blockchain.views import (
    BlockchainActorsView,
    BlockchainArchitectureView,
    BlockchainRecordFlowView,
    MockExternalAPIsView,
    BlockchainDemoTransactionView,
    BlockchainLedgerStateView,
    BlockchainTransactionsView,
    BlockchainAuditTrailView
)

urlpatterns = [
    path('actors/', BlockchainActorsView.as_view(), name='blockchain-actors'),
    path('architecture/', BlockchainArchitectureView.as_view(), name='blockchain-architecture'),
    path('record-flow/', BlockchainRecordFlowView.as_view(), name='blockchain-record-flow'),
    path('mock-external-apis/', MockExternalAPIsView.as_view(), name='blockchain-mock-apis'),
    path('demo-transaction/', BlockchainDemoTransactionView.as_view(), name='blockchain-demo-tx'),
    path('ledger-state/<str:request_id>/', BlockchainLedgerStateView.as_view(), name='blockchain-ledger-state'),
    path('transactions/', BlockchainTransactionsView.as_view(), name='blockchain-transactions'),
    path('audit-trail/<str:user_id>/', BlockchainAuditTrailView.as_view(), name='blockchain-audit-trail'),
]
