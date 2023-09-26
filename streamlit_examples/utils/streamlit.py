import os
import streamlit as st

CACHE_DIR = "./uploads"


def render_message(message):
    with st.chat_message(message["role"]):
        st.write(message["text"])


def get_key():
    if "openai_api_key" not in st.session_state:
        openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        st.session_state["openai_api_key"] = openai_api_key
    return st.session_state["openai_api_key"]


def upload_files(type="pdf", **kwargs):
    files = st.file_uploader(
        label=f"Upload {type.upper()} files", type=[type], **kwargs
    )
    if not files:
        st.info(f"Please add {type.upper()} documents")
        st.stop()
    return files


def cache_files(files, type="pdf") -> list[str]:
    filepaths = []
    for file in files:
        filepath = cache_file(file, type=type)
        filepaths.append(filepath)
    return filepaths


def cache_file(file, type="pdf") -> str:
    filepath = f"{CACHE_DIR}/{file.file_id}.{type}"
    if not os.path.exists(filepath):
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
    return filepath
