import face_recognition
import cv2
import os
import glob
import numpy as np

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def load_encoding_images(self, images_path):
        print("[INFO] Loading known faces...")
        for file_path in glob.glob(os.path.join(images_path, "*.*")):
            image = face_recognition.load_image_file(file_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                self.known_face_encodings.append(encoding[0])
                name = os.path.splitext(os.path.basename(file_path))[0]
                self.known_face_names.append(name)
                print(f"[INFO] Loaded: {name}")
            else:
                print(f"[WARNING] No face found in {file_path}")

    def detect_known_faces(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        return face_locations, face_names
