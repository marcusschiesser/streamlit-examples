import os
from PIL import Image
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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def initPage(page_title):
    dir_root = os.path.dirname(os.path.abspath(__file__))
    logo = Image.open(dir_root+'/../assets/logo.png')
    favicon = Image.open(dir_root+'/../assets/favicon.png')
    st.set_page_config(page_title=page_title, page_icon=favicon)
    local_css("style.css")
    st.sidebar.image(logo)