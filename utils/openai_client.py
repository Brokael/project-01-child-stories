import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


@lru_cache(maxsize=1)
def get_openai_client():
    api_key = get_openai_api_key()

    if not api_key:
        raise RuntimeError(
            "Missing OpenAI API key. Set OPENAI_API_KEY in your local .env file "
            "or in Streamlit Cloud secrets."
        )

    return OpenAI(api_key=api_key)
