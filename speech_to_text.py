import os
import tempfile

import streamlit as st
import whisper


@st.cache_resource
def load_whisper_model():
    print("Loading Whisper model...")
    return whisper.load_model("tiny")


def transcribe_audio(audio_bytes):
    if not audio_bytes:
        return ""

    temp_path = None

    try:
        # Save microphone recording temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_file:

            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        # Load Whisper
        model = load_whisper_model()

        # Transcribe
        result = model.transcribe(
            temp_path,
            fp16=False,
            language="en"
        )

        return result.get("text", "").strip()

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)