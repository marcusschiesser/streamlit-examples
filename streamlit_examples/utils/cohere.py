import cohere
import streamlit as st

cohere_api_key = st.secrets["cohere_api_key"]


@st.cache_resource(show_spinner="Connecting to Cohere...")
def connect_cohere():
    return cohere.Client(cohere_api_key)


def summarize(text: str) -> str:
    if len(text) <= 250:
        # Cohere's API requires at least 250 characters
        return text
    response = connect_cohere().summarize(
        text=text,
        length="auto",
        format="auto",
        model="command",
        additional_command="",
        temperature=0.8,
    )
    return response.summary
