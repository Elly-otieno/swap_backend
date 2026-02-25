from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lines.models import Line
from swap.models import SwapSession
from swap.serializers import StartSwapSerializer
from swap.services.eligibility import is_swap_allowed
from audit.services import log_audit

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

        return Response({
            "allowed": True,
            "session_id": session.id,
            "next_step": "PRIMARY"
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

        if session.stage != "ID_PASSED":
            return Response({"error": "Invalid stage"}, status=400)

        session.stage = "COMPLETED"
        session.save()

        from blockchain.services import log_event
        log_event("SWAP_COMPLETED", session.line.msisdn)

        return Response({"success": True})