from django.contrib import admin
from django.urls import path
from swap.views import StartSwapView
from vetting.views import (
    PrimaryVettingView,
    SecondaryVettingView,
    FaceScanView,
    IDScanView,
)
from swap.views import CompleteSwapView
from customers.views import AllCustomersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("swap/start/", StartSwapView.as_view()),
    path("swap/primary/", PrimaryVettingView.as_view()),
    path("swap/secondary/", SecondaryVettingView.as_view()),
    path("swap/face/", FaceScanView.as_view()),
    path("swap/id/", IDScanView.as_view()),
    path("swap/complete/", CompleteSwapView.as_view()),
    path("all/", AllCustomersView.as_view(), name="all-customers"),
]
