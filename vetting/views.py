from django.shortcuts import render

from vetting.services.primary import evaluate_primary
from swap.services.lock import lock_session
from swap.models import SwapSession
from rest_framework.views import APIView
from rest_framework.response import Response
from vetting.serializers import PrimarySerializer, SecondarySerializer
from rest_framework.parsers import MultiPartParser, FormParser

from vetting.services.biometric import validate_face, validate_id

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
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        session_id = request.data.get("session_id")
        # Matches the 'face_image' key  used in FormData
        uploaded_image = request.FILES.get("face_image") 
    
        if uploaded_image:
            print("--- IMAGE DEBUG ---")
            print(f"File Name: {uploaded_image.name}")
            print(f"Content Type: {uploaded_image.content_type}")
            print(f"Size: {uploaded_image.size} bytes")
            
            # Check if the file is empty
            if uploaded_image.size == 0:
                print("ERROR: Received 0 bytes. Upload failed.")
            
            # Peek at the first 10 bytes to see if it's actually a JPEG
            # JPEGs usually start with \xff\xd8
            uploaded_image.seek(0)
            peek = uploaded_image.read(10)
            print(f"Header Peek: {peek}")
            uploaded_image.seek(0) # IMPORTANT: Reset after reading!
            print("-------------------")
        else:
            print("ERROR: No 'face_image' found in request.FILES")

        if not session_id or not uploaded_image:
            return Response(
                {"error": "session_id and face_image are required"}, 
                status=400
            )

        try:
            session = SwapSession.objects.select_related('line__customer').get(id=session_id)
        except SwapSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)

        if session.is_locked:
            return Response({"locked": True, "redirect": "retail", "message": "Account is locked."})

        # Update attempt counter
        session.face_attempts += 1
        
        # Call the simplified image validation
        passed, message = validate_face(session, uploaded_image)

        if passed:
            session.stage = "FACE_PASSED"
            session.save()
            return Response({
                "passed": True, 
                "next_step": "ID",
                "message": message
            })

        # Failure & Locking Logic
        if session.face_attempts >= 3: # Given it's a still image, maybe allow 3 tries
            lock_session(session, "FACE_FAILED")
            return Response({
                "locked": True, 
                "redirect": "retail", 
                "message": f"Verification failed: {message}. Please visit Safaricom retail."
            })

        session.stage = "FACE_FAILED"
        session.save()

        return Response({
            "passed": False, 
            "remaining_attempts": 3 - session.face_attempts,
            "message": message
        })

class IDScanView(APIView):

    def post(self, request):
        session = SwapSession.objects.get(id=request.data["session_id"])

        if session.is_locked:
            return Response({"redirect": "retail"})

        session.id_attempts += 1

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

