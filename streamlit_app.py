import streamlit as st
import whisper
import os
import ffmpeg  # Explicitly import ffmpeg

# Check FFmpeg installation
try:
    ffmpeg.probe("temp_audio.mp3") # or any audio file
    print("FFmpeg installed and working.")
except Exception as e:
    print(f"FFmpeg problem: {e}")
    st.error("FFmpeg is not installed or not working properly. Please check your environment.")
    st.stop() # Stop app execution if FFmpeg has issues

# Initialize the Whisper model (do this once)
try:
    import whisper
    whisper._MODELS = whisper._download_models(whisper._MODELS) # Download models if necessary.
    model = whisper.load_model("base")

except Exception as e:
    st.error(f"Error loading Whisper model: {e}")  # Display error message in Streamlit
    st.stop()


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
