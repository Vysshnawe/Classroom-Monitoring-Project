import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

class FaceRecognizer:

    def __init__(self,dataset_path):

        self.dataset_path = dataset_path

        self.app = FaceAnalysis(name="buffalo_s")
        self.app.prepare(ctx_id=-1, det_size=(416,416))

        self.student_ids = []
        self.embeddings = []

        self.load_dataset()

    def load_dataset(self):

        for file in os.listdir(self.dataset_path):

            path = os.path.join(self.dataset_path,file)

            img = cv2.imread(path)

            faces = self.app.get(img)

            if len(faces)==0:
                continue

            emb = faces[0].embedding

            student_id = os.path.splitext(file)[0]

            self.student_ids.append(student_id)
            self.embeddings.append(emb)

        self.embeddings = np.array(self.embeddings)

    def detect_faces(self,frame):

        return self.app.get(frame)

    def recognize(self,embedding):

        sims = cosine_similarity([embedding],self.embeddings)[0]

        idx = np.argmax(sims)

        if sims[idx] > 0.45:
            return self.student_ids[idx],sims[idx]

        return None,0