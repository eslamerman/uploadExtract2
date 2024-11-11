import streamlit as st
import whisper
import os
import subprocess

# Check FFmpeg installation using subprocess
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

# Verify FFmpeg at startup
if not check_ffmpeg():
    st.error("FFmpeg is not installed or not working properly. Please check your environment.")
    st.stop()

# Initialize the Whisper model (do this once)
try:
    model = whisper.load_model("base")
except Exception as e:
    st.error(f"Error loading Whisper model: {e}")
    st.stop()

def transcribe_audio(audio_file):
    """Transcribes audio from an uploaded MP3 file using Whisper."""
    try:
        # Save uploaded file
        temp_path = "temp_audio.mp3"
        with open(temp_path, "wb") as temp_file:
            temp_file.write(audio_file.read())
        
        # Perform transcription
        result = model.transcribe(temp_path)
        text = result["text"]
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return text
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None

# Streamlit app
st.title("Audio Transcription")
uploaded_file = st.file_uploader("Choose an MP3 audio file", type=["mp3"])

if uploaded_file is not None:
    transcribed_text = transcribe_audio(uploaded_file)
    if transcribed_text:
        st.header("Transcribed Text")
        st.text_area(" ", transcribed_text, height=300)
