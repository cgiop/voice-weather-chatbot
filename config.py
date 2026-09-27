import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_api_key(name: str) -> str | None:
    """Read a key from local .env first, then Streamlit Secrets."""
    value = os.getenv(name)

    if value:
        return value

    try:
        return st.secrets[name]
    except (KeyError, FileNotFoundError):
        return None
