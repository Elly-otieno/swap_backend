from django.contrib import admin
from django.urls import path, include
from swap.views import StartSwapView
from vetting.views import (
    PrimaryVettingView,
    DiditWebhookView,
    # SecondaryVettingView,
    # FaceScanView,
    # IDScanView,
)
from swap.views import CompleteSwapView, SwapSessionStatusView
from customers.views import AllCustomersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("swap/start/", StartSwapView.as_view()),
    path("swap/primary/", PrimaryVettingView.as_view()),
    # path("swap/secondary/", SecondaryVettingView.as_view()),
    # path("swap/face/", FaceScanView.as_view()),
    # path("swap/id/", IDScanView.as_view()),
    path("swap/complete/", CompleteSwapView.as_view()),
    path("all/", AllCustomersView.as_view(), name="all-customers"),
    path("didit/webhook/", DiditWebhookView.as_view(), name="didit-webhook"),
    path("swap/session/<int:session_id>/", SwapSessionStatusView.as_view(), name="session-status"),
    path("api/v1/blockchain/", include('blockchain.urls')),
]
