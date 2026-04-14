import streamlit as st
import face_recognition
import numpy as np
import pandas as pd
from PIL import Image

st.title("Criminal Detection System using Face Recognition")

# Load dataset safely
try:
    data = pd.read_csv("dataset.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Check required columns
required_columns = ["name", "crime_status"]
if not all(col in data.columns for col in required_columns):
    st.error("CSV must contain 'name' and 'crime_status' columns")
    st.stop()

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        # Load image and convert to RGB
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Convert to numpy array
        img = np.array(image)

        # Detect faces
        face_locations = face_recognition.face_locations(img)

        if len(face_locations) > 0:
            st.success(f"Face Detected! ({len(face_locations)} face(s))")

            # 🔴 DEMO LOGIC (random selection)
            detected_person = data.sample(1).iloc[0]

            st.subheader("Detection Result")
            st.write(f"Name: {detected_person['name']}")
            st.write(f"Status: {detected_person['crime_status']}")

            if detected_person['crime_status'].lower() == "criminal":
                st.error("⚠️ Criminal Detected!")
            else:
                st.success("No Criminal Record Found")

        else:
            st.warning("No face detected in the image")

    except Exception as e:
        st.error(f"Error processing image: {e}")

        import streamlit as st
from main import load_images

st.title("Face Recognition System")

images, classNames = load_images()

st.write("Loaded Names:")
st.write(classNames)