from io import BytesIO

from gtts import gTTS


def text_to_speech(text: str) -> bytes:
    """Convert response text into MP3 bytes."""
    if not text.strip():
        raise ValueError("Cannot synthesize empty text.")

    audio_buffer = BytesIO()
    gTTS(text=text, lang="en").write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.read()
