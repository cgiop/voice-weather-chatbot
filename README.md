# 🌦️ Voice Weather Assistant

A beginner-friendly Streamlit voice weather chatbot.

## What it does

The final app supports:

1. Text weather questions.
2. Gemini-based city extraction.
3. Microphone recording with Streamlit.
4. Local Whisper speech-to-text.
5. Live current weather from OpenWeatherMap.
6. Gemini-generated natural-language responses grounded in the returned weather data.
7. gTTS voice output.
8. Conversation history.

## Architecture

```text
User voice
   ↓
Streamlit microphone
   ↓
Whisper
   ↓
Recognized text
   ↓
Gemini → city extraction
   ↓
OpenWeatherMap
   ↓
Weather facts
   ↓
Gemini → concise response
   ↓
gTTS
   ↓
Audio player
```

The weather API is the source of weather facts. Gemini is instructed to use only those facts.

---

# 1. Prerequisites

Recommended Python: 3.12 for current Streamlit Community Cloud compatibility.

Install Python from python.org if necessary.

Whisper also requires `ffmpeg`.

### Windows

If you use Winget:

```powershell
winget install ffmpeg
```

Or with Chocolatey:

```powershell
choco install ffmpeg
```

Verify:

```powershell
ffmpeg -version
```

---

# 2. Create the project

```text
voice-weather-chatbot/
├── app.py
├── weather.py
├── chatbot.py
├── speech_to_text.py
├── text_to_speech.py
├── config.py
├── requirements.txt
├── packages.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

# 4. API keys

Create `.env` from `.env.example`.

```env
OPENWEATHER_API_KEY=your_openweathermap_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env`.

For Gemini, create an API key in Google AI Studio.

For OpenWeatherMap, create an API key in your OpenWeatherMap account.

---

# 5. Development stages

## Stage 1 — Weather API

Start with:

```bash
streamlit run app.py
```

Type:

```text
Chennai
```

or:

```text
What's the weather in Chennai?
```

The final `app.py` includes the text fallback, but the underlying Stage 1 component is `weather.py`.

You can independently test it from Python:

```python
from config import get_api_key
from weather import get_weather

key = get_api_key("OPENWEATHER_API_KEY")
print(get_weather("Chennai", key))
```

Expected fields:

- temperature
- feels-like temperature
- condition
- humidity
- wind speed

### Common Stage 1 errors

**Invalid API key**

Check `.env` and make sure the key is active.

**City not found**

Try a clearer city name such as `Chennai, India`.

**Connection error**

Check your internet connection.

---

## Stage 2 — Natural Language Understanding

Gemini receives:

```text
Can you tell me the weather in Chennai?
```

and returns:

```text
Chennai
```

The extracted city is then passed to `weather.py`.

Test examples:

```text
What's the weather in Bangalore?
How hot is Mumbai?
Tell me the current weather in Delhi.
```

If Gemini returns a sentence instead of a city, the extraction prompt is deliberately strict and the application also trims the first line.

---

## Stage 3 — Speech-to-Text

The Streamlit microphone widget records audio at 16 kHz.

The audio is passed to local Whisper:

```python
model = whisper.load_model("tiny")
```

Then Whisper returns text such as:

```text
What's the weather in Chennai?
```

Test:

1. Open the Streamlit app.
2. Allow microphone access.
3. Click the recording widget.
4. Say a short sentence.
5. Stop recording.
6. Check the **You said** section.

Whisper's official setup requires `ffmpeg`; Streamlit Community Cloud can install Linux dependencies through `packages.txt`.

### Common Stage 3 errors

**Microphone does not work**

Allow microphone permission in your browser.

**Whisper cannot load**

Make sure:

```bash
pip install openai-whisper
```

worked and `ffmpeg -version` works.

**Whisper is slow**

Use the `tiny` model. It is intentionally chosen here for a beginner-friendly CPU deployment.

---

## Stage 4 — Natural Response

The weather dictionary is sent to Gemini.

Gemini is explicitly told:

- weather facts come from OpenWeatherMap;
- do not invent missing weather information;
- answer in 1-3 sentences.

Example:

```text
The current temperature in Chennai is 29.0 °C.
It's partly cloudy with 72% humidity.
```

This separation is important:

```text
OpenWeatherMap → facts
Gemini → wording
```

---

## Stage 5 — Text-to-Speech

The final response is passed to gTTS.

The resulting MP3 is displayed with:

```python
st.audio(...)
```

The full flow becomes:

```text
🎤 Voice
   ↓
Whisper
   ↓
Text
   ↓
Gemini city extraction
   ↓
OpenWeatherMap
   ↓
Weather facts
   ↓
Gemini response
   ↓
gTTS
   ↓
🔊 Audio
```

---

# 6. Run locally

From the project root:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit.

---

# 7. Deployment to Streamlit Community Cloud

Push the project to GitHub.

Do NOT push:

```text
.env
.streamlit/secrets.toml
```

The repository should contain:

```text
app.py
weather.py
chatbot.py
speech_to_text.py
text_to_speech.py
config.py
requirements.txt
packages.txt
.env.example
.gitignore
README.md
```

In Streamlit Community Cloud:

1. Open your Streamlit workspace.
2. Choose **Create app**.
3. Select the GitHub repository.
4. Select the branch.
5. Select `app.py` as the entrypoint.
6. Open **Advanced settings**.
7. Select a supported Python version, such as Python 3.12.
8. Add the secrets below.
9. Deploy.

Secrets:

```toml
OPENWEATHER_API_KEY = "your_openweathermap_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
```

The application reads environment variables locally and Streamlit Secrets when deployed.

---

# 8. Troubleshooting deployment

## `ffmpeg` not found

Make sure the repository contains:

```text
packages.txt
```

with:

```text
ffmpeg
```

## `ModuleNotFoundError`

Check `requirements.txt` and redeploy after committing changes.

## API key errors

Open your deployed app's settings and update its Secrets.

## Microphone permission

Browser microphone permission is controlled by the browser/device. Allow microphone access for the Streamlit site.

## Whisper takes a while on first use

The Whisper model is downloaded and loaded the first time it is needed. `st.cache_resource` prevents the model from being loaded repeatedly during normal Streamlit reruns.

---

# 9. Security

Never put API keys in:

- `app.py`
- `weather.py`
- `chatbot.py`
- GitHub commits
- screenshots
- README files

Use `.env` locally and Streamlit Secrets in deployment.

---

# 10. Beginner mental model

Think of the application as five small programs connected together:

```text
1. WEATHER
city → OpenWeatherMap → weather dictionary

2. NLP
question → Gemini → city

3. SPEECH
microphone → Whisper → question

4. RESPONSE
weather dictionary + question → Gemini → answer

5. VOICE
answer → gTTS → MP3
```

The Streamlit app simply connects these pieces.

---

## Important limitation

This project answers **current weather** using OpenWeatherMap's current-weather endpoint. A question such as "Will it rain tomorrow?" needs a forecast endpoint and additional logic; the current version should not invent a forecast from current conditions.
