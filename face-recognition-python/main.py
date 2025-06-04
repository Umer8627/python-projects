import cv2
from simple_facerec import SimpleFacerec

# Initialize face recognition
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

process_this_frame = True

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera disconnected or frame error.")
        break

    if process_this_frame:
        face_locations, face_names = sfr.detect_known_faces(frame)

    process_this_frame = not process_this_frame  # Skip every other frame

    # Draw boxes and names
    if 'face_locations' in locals():
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Label background
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
            # Label text
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    # Show frame
    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(1)
    if key == ord('q') or cv2.getWindowProperty('Face Recognition', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()

# img = cv2.imread("Messi1.PNG")
# rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img_encoding = face_recognition.face_encodings(rgb_img)[0]


# img2 = cv2.imread("images/Messi.PNG")
# rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
# img2_encoding = face_recognition.face_encodings(rgb_img2)[0]

# results =face_recognition.compare_faces([img_encoding], img2_encoding)
# print('Match:', results[0])

# cv2.imshow("Img", img)
# cv2.imshow("Img 2", img2)
# cv2.waitKey(0)