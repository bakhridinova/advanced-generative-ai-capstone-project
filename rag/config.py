import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_env_setting(config_key: str) -> str:
    env_value = os.getenv(config_key)
    if not env_value and hasattr(st, 'secrets') and config_key in st.secrets:
        env_value = st.secrets[config_key]
    return env_value


API_KEY_OPENAI = get_env_setting("OPENAI_API_KEY")
TOKEN_GITHUB = get_env_setting("GITHUB_TOKEN")
REPOSITORY_GITHUB = get_env_setting("GITHUB_REPO")
MODEL_NAME = get_env_setting("LLM_MODEL") or "gpt-4o-mini"

PATH_VECTOR_DB = "chroma_db"
PATH_DOCUMENTS = "documents"

TEXT_CHUNK_SIZE = 1050
TEXT_CHUNK_OVERLAP = 120
