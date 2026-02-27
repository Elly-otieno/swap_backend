from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lines.models import Line
from swap.models import SwapSession
from swap.serializers import StartSwapSerializer
from swap.services.eligibility import is_swap_allowed
from audit.services import log_audit
from blockchain.services import blockchain_service

class StartSwapView(APIView):

    def post(self, request):
        serializer = StartSwapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        msisdn = serializer.validated_data["msisdn"]

        try:
            line = Line.objects.select_related("customer").get(msisdn=msisdn)
        except Line.DoesNotExist:
            return Response({"allowed": False, "reason": "Line not found"})

        allowed, reason = is_swap_allowed(line)

        if not allowed:
            return Response({"allowed": False, "reason": reason})

        # Check for locked session
        existing_locked = SwapSession.objects.filter(
            line=line,
            is_locked=True
        ).exists()

        if existing_locked:
            return Response({
                "allowed": False,
                "redirect": "retail"
            })

        session = SwapSession.objects.create(
            line=line,
            stage="STARTED"
        )

        log_audit(msisdn, "SWAP_STARTED")

        # Blockchain Integration: Initiate SIM swap
        old_sim_serial = "old_sim_serial_mock"
        new_sim_serial = "new_sim_serial_mock"

        swap_result = blockchain_service.initiate_sim_swap(
            request_id=str(session.id),
            user_id=str(line.customer.id),
            phone_number=msisdn,
            old_sim_serial=old_sim_serial,
            new_sim_serial=new_sim_serial
        )

        session.swap_id = swap_result.get("swapId") or "0x0"
        session.save()

        return Response({
            "allowed": True,
            "session_id": session.id,
            "next_step": "PRIMARY",
            "swapId": session.swap_id,
            "txHash": swap_result.get("txHash")
        })

class SwapSessionStatusView(APIView):
    def get(self, request, session_id):
        session = SwapSession.objects.get(id=session_id)

        return Response({
            "stage": session.stage,
            "locked": session.is_locked,
        })

class CompleteSwapView(APIView):

    def post(self, request):
        session = SwapSession.objects.get(id=request.data["session_id"])

        if session.stage != "DIDIT_PASSED":
            return Response({"error": "Invalid stage"}, status=400)

        # Mark session completed
        session.stage = "COMPLETED"
        session.save()
        
        # Legacy audit/logging
        blockchain_service.log_event("SWAP_COMPLETED", session.line.msisdn)

        # Real or demo blockchain approval
        # Ensure swap_id exists for demo-safe operation
        swap_id = getattr(session, "swap_id", str(session.id))  # fallback to session.id if missing
        blockchain_service.approve_sim_swap(str(session.id), swap_id)

        return Response({"success": True})