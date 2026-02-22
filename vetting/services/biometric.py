import cv2
import numpy as np
import face_recognition

def validate_face(session, uploaded_image):
    try:
        customer = session.line.customer
        if not customer or not customer.id_photo:
            return False, "No reference ID photo found."

        # --- 1. PROCESS LIVE IMAGE ---
        uploaded_image.seek(0)
        file_bytes = np.frombuffer(uploaded_image.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return False, "Failed to decode image."

        # Force convert to RGB and ensure exactly 3 channels
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Slicing [:, :, :3] ensures we strip any hidden Alpha channels 
        # .astype(np.uint8) ensures 8-bit depth
        live_final = np.array(img[:, :, :3], dtype='uint8')

        # --- 2. PROCESS REFERENCE IMAGE ---
        ref_path = customer.id_photo.path
        ref_img = cv2.imread(ref_path)
        if ref_img is None:
            return False, "Reference ID photo unreadable."
            
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)
        ref_final = np.array(ref_img[:, :, :3], dtype='uint8')

        # DEBUG PRINTS - Check these in your terminal!
        print(f"DEBUG: Live Shape: {live_final.shape}, Dtype: {live_final.dtype}")
        print(f"DEBUG: Ref Shape: {ref_final.shape}, Dtype: {ref_final.dtype}")

        # --- 3. GENERATE ENCODINGS ---
        live_encodings = face_recognition.face_encodings(live_final)
        ref_encodings = face_recognition.face_encodings(ref_final)

        if not live_encodings:
            return False, "No face detected in scan. Position your face in the oval."
        if not ref_encodings:
            return False, "Could not process biometrics from ID photo."

        # --- 4. COMPARE ---
        results = face_recognition.compare_faces([ref_encodings[0]], live_encodings[0], tolerance=0.5)

        return (True, "Verified") if results[0] else (False, "Face mismatch.")

    except Exception as e:
        print(f"CRITICAL: {e}")
        return False, "Internal verification error."

def validate_id(scan_data):
    """
    Expected payload:
    {
        "ocr_match_score": 0.92,
        "id_number_match": True
    }
    """

    score = scan_data.get("ocr_match_score", 0)
    id_match = scan_data.get("id_number_match", False)

    if score >= 0.85 and id_match:
        return True

    return False

