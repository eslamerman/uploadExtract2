import streamlit as st
import easyocr
import cv2
from PIL import Image  # For image processing with EasyOCR
import numpy as np # For handling OpenCV image formats



# Initialize EasyOCR reader (do this once)
reader = easyocr.Reader(['en'])  # Specify language(s)



def extract_text_from_uploaded_video(uploaded_file):
    """Extracts text from an uploaded video file directly using EasyOCR."""
    try:
        # Create a temporary file to store the uploaded video
        with open("temp_video.mp4", "wb") as temp_file: 
            temp_file.write(uploaded_file.read()) # Write the uploaded file contents

        cap = cv2.VideoCapture("temp_video.mp4")
        extracted_text = ""

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                pil_image = Image.fromarray(frame)
                ocr_results = reader.readtext(pil_image)

                for result in ocr_results:
                    extracted_text += result[1] + " "

            else:
                break 

        cap.release()
        os.remove("temp_video.mp4") # Clean up

        return extracted_text

    except Exception as e:
        st.error(f"Error extracting text from video: {e}")
        return None




# Streamlit app
st.title("Video Text Extraction")


uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])  # Adjust file types


if uploaded_file is not None:

    extracted_text = extract_text_from_uploaded_video(uploaded_file)

    if extracted_text:
        st.header("Extracted Text")
        st.text_area(" ", extracted_text, height=300)
