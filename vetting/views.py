from django.shortcuts import render

from vetting.services.primary import evaluate_primary
from swap.services.lock import lock_session
from swap.models import SwapSession
from rest_framework.views import APIView
from rest_framework.response import Response
from vetting.serializers import PrimarySerializer, SecondarySerializer

class PrimaryVettingView(APIView):

    def post(self, request):
        serializer = PrimarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = SwapSession.objects.select_related(
            "line__customer"
        ).get(id=serializer.validated_data["session_id"])

        if session.is_locked:
            return Response({"redirect": "retail"})

        customer = session.line.customer

        session.primary_attempts += 1

        passed = evaluate_primary(customer, serializer.validated_data)

        if not passed:
            lock_session(session, "PRIMARY_FAILED")
            return Response({
                "passed": False,
                "locked": True,
                "redirect": "retail"
            })

        session.stage = "PRIMARY_PASSED"
        session.save()

        return Response({
            "passed": True,
            "next_step": "FACE"
        })


from vetting.services.secondary import evaluate_secondary

class SecondaryVettingView(APIView):

    def post(self, request):
        serializer = SecondarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = SwapSession.objects.select_related(
            "line__customer"
        ).get(id=serializer.validated_data["session_id"])

        if session.is_locked:
            return Response({"redirect": "retail"})

        session.secondary_attempts += 1

        wallet = session.line.customer.walletprofile

        passed = evaluate_secondary(
            session.line.customer,
            wallet,
            serializer.validated_data["answers"]
        )

        if passed:
            session.stage = "SECONDARY_PASSED"
            session.save()

            return Response({
                "passed": True,
                "next_step": "FACE"
            })

        if session.secondary_attempts >= 2:
            lock_session(session, "SECONDARY_FAILED")

            return Response({
                "passed": False,
                "locked": True,
                "redirect": "retail"
            })

        session.stage = "SECONDARY_FAILED"
        session.save()

        return Response({
            "passed": False,
            "remaining_attempts": 1
        })


class FaceScanView(APIView):

    def post(self, request):
        session = SwapSession.objects.get(id=request.data["session_id"])

        if session.is_locked:
            return Response({"redirect": "retail"})

        session.face_attempts += 1

        from vetting.services.biometric import validate_face

        if validate_face(request.data):
            session.stage = "FACE_PASSED"
            session.save()
            return Response({"passed": True, "next_step": "ID"})

        if session.face_attempts >= 2:
            lock_session(session, "FACE_FAILED")
            return Response({"locked": True, "redirect": "retail"})

        session.stage = "FACE_FAILED"
        session.save()

        return Response({"passed": False, "remaining_attempts": 1})


class IDScanView(APIView):

    def post(self, request):
        session = SwapSession.objects.get(id=request.data["session_id"])

        if session.is_locked:
            return Response({"redirect": "retail"})

        session.id_attempts += 1

        from vetting.services.biometric import validate_id

        if validate_id(request.data):
            session.stage = "ID_PASSED"
            session.save()
            return Response({"passed": True, "next_step": "COMPLETE"})

        if session.id_attempts >= 2:
            lock_session(session, "ID_FAILED")
            return Response({"locked": True, "redirect": "retail"})

        session.stage = "ID_FAILED"
        session.save()

        return Response({"passed": False, "remaining_attempts": 1})

