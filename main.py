import cv2
import os
import numpy as np
import pandas as pd
import sys
import json
from tqdm import tqdm
from datetime import datetime

from recognizer import FaceRecognizer
from attentiveness import AttentivenessEstimator
from utils import format_time



if len(sys.argv) < 4:
    print("Usage: python main.py <video_path> <dataset_path> <output_path>")
    sys.exit(1)
VIDEO_PATH = sys.argv[1]
DATASET_PATH = sys.argv[2]
SESSION_OUTPUT = sys.argv[3]

OUTPUT_VIDEO = os.path.join(SESSION_OUTPUT, "output_video.mp4")

recognizer = FaceRecognizer(DATASET_PATH)
attn = AttentivenessEstimator()

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS) or 30
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))




duration_sec = total_frames / fps

if duration_sec > 600:
    FRAME_SKIP = 60
elif duration_sec < 15:
    FRAME_SKIP = 5
else:
    FRAME_SKIP = 30

seconds_per_check = FRAME_SKIP / fps



RESIZE_WIDTH = 720
scale = RESIZE_WIDTH / width
resized_height = int(height * scale)


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))


attendance = {}
first_seen = {}

student_total_frames = {}
student_attentive_frames = {}

distraction_time = {}
down_time = {}
laugh_time = {}

timeline_data = []

frame_id = 0


print(f"Processing Video (Length: {duration_sec:.1f}s, Skip: {FRAME_SKIP})...")


for _ in tqdm(range(total_frames)):

    ret, frame = cap.read()

    if not ret:
        break

    frame_id += 1

    if frame_id % FRAME_SKIP != 0:
        out.write(frame)
        continue


    small_frame = cv2.resize(frame, (RESIZE_WIDTH, resized_height))

    faces = recognizer.detect_faces(small_frame)

    current_frame_attentive_count = 0


    for face in faces:

        bbox, embedding, landmarks = face.bbox.astype(int), face.embedding, face.kps

        x1, y1, x2, y2 = [int(v / scale) for v in bbox]

        student_id, sim = recognizer.recognize(embedding)

        if student_id is None:
            continue


       

        if student_id not in attendance:
            attendance[student_id] = "Yes"
            first_seen[student_id] = format_time(frame_id / fps)


      

        left_eye = landmarks[0]
        right_eye = landmarks[1]
        nose = landmarks[2]
        left_mouth = landmarks[3]
        right_mouth = landmarks[4]


        eye_center_y = (left_eye[1] + right_eye[1]) / 2

        eye_distance = np.linalg.norm(left_eye - right_eye)

        if eye_distance == 0:
            continue


        vertical_ratio = (nose[1] - eye_center_y) / eye_distance

        mouth_width = np.linalg.norm(left_mouth - right_mouth)

        mouth_ratio = mouth_width / eye_distance


        

        if student_id not in distraction_time:
            distraction_time[student_id] = 0

        if student_id not in down_time:
            down_time[student_id] = 0

        if student_id not in laugh_time:
            laugh_time[student_id] = 0



        if vertical_ratio > 0.55:
            down_time[student_id] += seconds_per_check
        else:
            down_time[student_id] = max(0, down_time[student_id] - seconds_per_check)


       
        if mouth_ratio > 0.85:
            laugh_time[student_id] += seconds_per_check
        else:
            laugh_time[student_id] = max(0, laugh_time[student_id] - seconds_per_check)


       

        base_focus = attn.is_attentive(landmarks)


       

        if down_time[student_id] > 12:
            distracted = True

        elif laugh_time[student_id] > 5:
            distracted = True

        else:
            distracted = not base_focus



        if distracted:
            distraction_time[student_id] += seconds_per_check
        else:
            distraction_time[student_id] = max(0, distraction_time[student_id] - seconds_per_check)


        is_truly_attentive = distraction_time[student_id] < 8


        
        if student_id not in student_total_frames:
            student_total_frames[student_id] = 0
            student_attentive_frames[student_id] = 0


        student_total_frames[student_id] += 1


        if is_truly_attentive:
            student_attentive_frames[student_id] += 1
            current_frame_attentive_count += 1


        percent = int(
            (student_attentive_frames[student_id] /
             student_total_frames[student_id]) * 100
        )


        color = (0, 255, 0) if is_truly_attentive else (0, 0, 255)


        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)


        cv2.putText(
            frame,
            f"{student_id} | {percent}%",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )


    frame_focus = int(
        (current_frame_attentive_count / len(faces)) * 100
    ) if faces else 0


    timeline_data.append({
        "time": format_time(frame_id / fps),
        "score": frame_focus
    })


    out.write(frame)



cap.release()
out.release()





attendance_rows = [
    [s, "Yes" if s in attendance else "No", first_seen.get(s, "-")]
    for s in recognizer.student_ids
]


pd.DataFrame(
    attendance_rows,
    columns=["Roll No", "Present", "First Seen Time"]
).to_csv(os.path.join(SESSION_OUTPUT, "attendance.csv"), index=False)


overall_score = (
    sum(student_attentive_frames.values()) /
    sum(student_total_frames.values()) * 100
) if student_total_frames else 0


with open(os.path.join(SESSION_OUTPUT, 'stats.json'), 'w') as f:
    json.dump({
        "overall_focus": round(overall_score, 2),
        "present_count": len(attendance)
    }, f)


with open(os.path.join(SESSION_OUTPUT, 'timeline.json'), 'w') as f:
    json.dump(timeline_data, f)


att_rows = [
    [s, round(
        (student_attentive_frames[s] /
         student_total_frames[s]) * 100, 2)]
    for s in student_total_frames
]


pd.DataFrame(
    att_rows,
    columns=["Roll No", "Attentiveness %"]
).to_csv(os.path.join(SESSION_OUTPUT, "attentiveness.csv"), index=False)





import sqlite3


session_folder_name = os.path.basename(SESSION_OUTPUT)

parts = session_folder_name.rsplit('_', 2)

class_name = parts[0].replace('_', ' ')

session_date = datetime.now().strftime("%d %b %Y %I:%M %p")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))


conn.execute(
    '''INSERT INTO sessions 
       (class_name, video_path, session_date, total_students, avg_attentiveness)
       VALUES (?, ?, ?, ?, ?)''',
    (
        class_name,
        session_folder_name,
        session_date,
        len(attendance),
        round(overall_score, 2)
    )
)


conn.commit()
conn.close()


print(
    f"Results saved to DB — Class: {class_name}, "
    f"Students: {len(attendance)}, Score: {overall_score:.2f}%"
)