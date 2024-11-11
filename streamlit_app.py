import streamlit as st
import whisper
import os

# Initialize the Whisper model (do this once)
model = whisper.load_model("base")  # Or another model size like "small", "medium", "large"


def transcribe_audio(audio_file):
    """Transcribes audio from an uploaded MP3 file using Whisper."""
    try:
        with open("temp_audio.mp3", "wb") as temp_file:
            temp_file.write(audio_file.read())

        # Perform transcription
        result = model.transcribe("temp_audio.mp3")
        text = result["text"]

        os.remove("temp_audio.mp3")  # Clean up temporary file

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
