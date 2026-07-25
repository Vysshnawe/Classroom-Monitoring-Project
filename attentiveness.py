import numpy as np

class AttentivenessEstimator:

    def __init__(self):
        pass


    def is_attentive(self, landmarks):
        """
        Determines if a student is attentive based on facial landmarks.
        Landmarks order:
        [left_eye, right_eye, nose, left_mouth, right_mouth]
        """

        left_eye = landmarks[0]
        right_eye = landmarks[1]
        nose = landmarks[2]
        left_mouth = landmarks[3]
        right_mouth = landmarks[4]

        # ---- Eye center ----
        eye_center_x = (left_eye[0] + right_eye[0]) / 2
        eye_center_y = (left_eye[1] + right_eye[1]) / 2

        # ---- Eye distance for normalization ----
        eye_distance = np.linalg.norm(left_eye - right_eye)

        if eye_distance == 0:
            return False

        # ---------------------------------------------------
        # 1️⃣ Head turning detection (left / right)
        # ---------------------------------------------------

        nose_offset_x = abs(nose[0] - eye_center_x)
        horizontal_ratio = nose_offset_x / eye_distance


        # ---------------------------------------------------
        # 2️⃣ Looking down detection
        # ---------------------------------------------------

        nose_offset_y = nose[1] - eye_center_y
        vertical_ratio = nose_offset_y / eye_distance


        # ---------------------------------------------------
        # 3️⃣ Talking / smiling detection
        # ---------------------------------------------------

        mouth_width = np.linalg.norm(left_mouth - right_mouth)
        mouth_ratio = mouth_width / eye_distance


        # ---------------------------------------------------
        # 4️⃣ Head tilt detection
        # ---------------------------------------------------

        eye_slope = abs((right_eye[1] - left_eye[1]) / (right_eye[0] - left_eye[0] + 1e-6))


        # ---------------------------------------------------
        # Attentiveness rules (balanced thresholds)
        # ---------------------------------------------------

        looking_sideways = horizontal_ratio > 0.32
        looking_down = vertical_ratio > 0.52
        talking_or_laughing = mouth_ratio > 0.80
        head_tilted = eye_slope > 0.28


        distracted = (
            looking_sideways
            or looking_down
            or talking_or_laughing
            or head_tilted
        )


        return not distracted