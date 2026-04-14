import streamlit as st
import face_recognition
import numpy as np
import cv2
import os
from PIL import Image

st.set_page_config(page_title="Criminal Detection System", layout="centered")

st.title("🔍 Criminal Detection System using Face Recognition")

# ==============================
# Load Known Criminal Images
# ==============================
path = "criminal_images"
images = []
classNames = []

if not os.path.exists(path):
    st.error("❌ 'criminal_images' folder not found")
    st.stop()

for file in os.listdir(path):
    img = cv2.imread(f"{path}/{file}")
    if img is not None:
        images.append(img)
        classNames.append(os.path.splitext(file)[0])

# ==============================
# Encode Faces
# ==============================
@st.cache_data
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
    return encodeList

encodeListKnown = findEncodings(images)

st.success("✅ System Ready")

# ==============================
# Upload Image
# ==============================
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Detect faces
    face_locations = face_recognition.face_locations(img)
    encodesCurFrame = face_recognition.face_encodings(img, face_locations)

    if len(face_locations) == 0:
        st.warning("⚠️ No face detected")
    else:
        st.success(f"✅ {len(face_locations)} face(s) detected")

        # Convert to BGR for OpenCV drawing
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        for encodeFace, faceLoc in zip(encodesCurFrame, face_locations):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            name = "Unknown"

            if True in matches:
                matchIndex = matches.index(True)
                name = classNames[matchIndex]

            top, right, bottom, left = faceLoc

            # Draw box
            cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(img_bgr, name.upper(), (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Display result
            if name != "Unknown":
                st.error(f"🚨 Criminal Detected: {name}")
            else:
                st.success("✅ No Criminal Record Found")

        # Show result image
        result_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        st.image(result_img, caption="Detection Result", use_column_width=True)

        import cv2
import os

def load_images(path='Training_images'):
    images = []
    classNames = []

    myList = os.listdir(path)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    return images, classNames

import cv2
import face_recognition
import os

# Load criminal images
path = "criminal_images"
images = []
classNames = []

for file in os.listdir(path):
    img = cv2.imread(f"{path}/{file}")
    images.append(img)
    classNames.append(os.path.splitext(file)[0])

# Encode faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Complete")

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam not detected")
    exit()

print("✅ Webcam started - Press Q to exit")

while True:
    success, img = cap.read()
    if not success:
        print("❌ Camera error")
        break

    # Resize for speed
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Detect faces
    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodesCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        name = "Unknown"

        if True in matches:
            matchIndex = matches.index(True)
            name = classNames[matchIndex]

        # Scale back
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

        # Draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, name.upper(), (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Criminal Detection System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()