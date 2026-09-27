import hashlib
import base64
import streamlit as st
from intent_classifier import predict_intent
from config import get_api_key
from weather import WeatherAPIError, get_weather
from speech_to_text import transcribe_audio
from intent_classifier import predict_intent
from chatbot import extract_city, generate_weather_response
from weather import get_weather
from config import get_api_key
from text_to_speech import text_to_speech
if "current_city" not in st.session_state:
    st.session_state.current_city = ""

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None
weather_key = get_api_key("OPENWEATHER_API_KEY")
gemini_key = get_api_key("GEMINI_API_KEY")

st.set_page_config(
    page_title="Voice Weather Assistant",
    page_icon="🌦️",
)

st.title("🌦️ Voice Weather Assistant")



# Prevent the same recording from being processed
# multiple times during Streamlit reruns.
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


# ============================================
# MICROPHONE
# ============================================

st.subheader("🎤 Ask by voice")

audio = st.audio_input(
    "Record your weather question",
    sample_rate=16000
)


if audio is not None:

    audio_bytes = audio.getvalue()

    audio_hash = hashlib.sha256(
        audio_bytes
    ).hexdigest()

    # Only process a new recording
    if audio_hash != st.session_state.last_audio_hash:

        st.session_state.last_audio_hash = audio_hash

        # -------------------------
        # Whisper
        # -------------------------

        with st.spinner(
            "🎧 Understanding your speech..."
        ):

            try:

                transcript = transcribe_audio(audio_bytes)

                if transcript:
                    st.write("### 🗣️ Recognized Speech")
                    st.write(transcript)

                    intent, confidence = predict_intent(transcript)

                    st.write("### 🧠 Detected Intent")
                    st.write(intent)

                    st.write(
                        f"Confidence: {confidence:.2%}"
                    )

                    # -----------------------------
                    # Intent-based routing
                    # -----------------------------

                    if intent == "greeting":

                        response = "Hello! 👋 How can I help you with the weather?"


                    else:

                        # Extract city using Gemini
                        city = extract_city(
                            transcript,
                            gemini_key
                        )

                        if city:
                            st.session_state.current_city = city

                        elif st.session_state.current_city:
                            city = st.session_state.current_city

                        else:
                            city = ""

                        if not city:

                            response = (
                                "Sure! Which city would you like to know about?"
                            )

                        else:

                            # Get weather data
                            weather = get_weather(
                                city,
                                weather_key
                            )

                            # Generate response based on intent
                            response = generate_weather_response(
                                weather,
                                transcript,
                                intent,
                                gemini_key
                            )

                            st.write("### 🌦️ Weather")
                            st.json(weather)

                            st.write("### 🤖 Assistant")
                            st.write(response)
                            st.session_state.messages.append(
                                {
                                    "role": "user",
                                    "content": transcript
                                }
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )
                            audio = text_to_speech(response)

                            audio_base64 = base64.b64encode(audio).decode()

                            st.markdown(
                                f"""
                                <audio autoplay>
                                    <source
                                        src="data:audio/mp3;base64,{audio_base64}"
                                        type="audio/mp3"
                                    >
                                </audio>
                                """,
                                unsafe_allow_html=True
                            )
                    
                

            except Exception as e:

                st.error(
                    "Speech recognition failed. "
                )
                st.exception(e)

                transcript = ""


        if transcript:

            st.subheader("🗣️ You said")

            st.write(
                f'"{transcript}"'
            )

            # -------------------------
            # API keys
            # -------------------------

            weather_key = get_api_key(
                "OPENWEATHER_API_KEY"
            )

            gemini_key = get_api_key(
                "GEMINI_API_KEY"
            )

            if not weather_key:

                st.error(
                    "OPENWEATHER_API_KEY is missing."
                )

                st.stop()

            if not gemini_key:

                st.error(
                    "GEMINI_API_KEY is missing."
                )

                st.stop()


            # -------------------------
            # Gemini city extraction
            # -------------------------

            with st.spinner(
                "Understanding..."
            ):

                try:

                    city = extract_city(
                        transcript,
                        gemini_key
                    )

                except Exception:

                    st.error(
                        "I couldn't understand "
                        "the city."
                    )

                    st.stop()


            if not city:

                st.warning(
                    "I couldn't find a city "
                    "in your question."
                )

                st.stop()


            st.info(
                f"📍 City detected: **{city}**"
            )


            # -------------------------
            # Weather API
            # -------------------------

            try:

                with st.spinner(
                    f"Getting weather for {city}..."
                ):

                    weather = get_weather(
                        city,
                        weather_key
                    )

            except WeatherAPIError as e:

                st.error(str(e))

                st.stop()


            # -------------------------
            # Weather display
            # -------------------------

            st.subheader(
                f"Weather in {weather['city']}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🌡️ Temperature",
                f"{weather['temperature']:.1f} °C"
            )

            col2.metric(
                "🤗 Feels Like",
                f"{weather['feels_like']:.1f} °C"
            )

            col3.metric(
                "💧 Humidity",
                f"{weather['humidity']}%"
            )

            st.write(
                f"☁️ **Condition:** "
                f"{weather['condition'].title()}"
            )

            st.write(
                f"💨 **Wind:** "
                f"{weather['wind_speed']:.1f} m/s"
            )

        else:

            st.error(
                "I couldn't recognize your speech. "
                "Please try again."
            )


# ============================================
# TEXT FALLBACK
# ============================================

st.divider()

st.subheader("⌨️ Or type your question")

question = st.text_input(
    "Weather question",
    placeholder="What's the weather in Chennai?"
)


if st.button("Get Weather"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        weather_key = get_api_key(
            "OPENWEATHER_API_KEY"
        )

        gemini_key = get_api_key(
            "GEMINI_API_KEY"
        )

        try:

            city = extract_city(
                question,
                gemini_key
            )

            st.info(
                f"📍 City detected: **{city}**"
            )

            weather = get_weather(
                city,
                weather_key
            )

            st.subheader(
                f"Weather in {weather['city']}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🌡️ Temperature",
                f"{weather['temperature']:.1f} °C"
            )

            col2.metric(
                "🤗 Feels Like",
                f"{weather['feels_like']:.1f} °C"
            )

            col3.metric(
                "💧 Humidity",
                f"{weather['humidity']}%"
            )

            st.write(
                f"☁️ **Condition:** "
                f"{weather['condition'].title()}"
            )

            st.write(
                f"💨 **Wind:** "
                f"{weather['wind_speed']:.1f} m/s"
            )

        except Exception as e:

            st.error(
                "Something went wrong. "
                "Please check your question and API keys."
            )