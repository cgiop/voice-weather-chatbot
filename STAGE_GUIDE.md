# Incremental Build Guide

The final `app.py` contains the complete pipeline. If you want to build it exactly one stage at a time, use this order.

## Stage 1

Create:

- `app.py`
- `weather.py`
- `config.py`
- `requirements.txt`
- `.env`

Test only city input.

Core call:

```python
weather = get_weather("Chennai", api_key)
```

Do not add Gemini or Whisper yet.

## Stage 2

Add:

- `chatbot.py`

Flow:

```text
typed question
→ extract_city()
→ get_weather()
```

## Stage 3

Add:

- `speech_to_text.py`
- `packages.txt`

Flow:

```text
microphone
→ Whisper
→ transcript
→ extract_city()
→ weather
```

## Stage 4

Add:

```python
generate_weather_response(...)
```

The LLM receives weather facts, not permission to search for or invent weather.

## Stage 5

Add:

- `text_to_speech.py`

Flow:

```text
answer
→ gTTS
→ st.audio
```

After Stage 5, enable conversation history.

This staged approach makes debugging easier because each new component can be tested after the previous component is known to work.
