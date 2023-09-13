from llama_index.chat_engine.types import StreamingAgentChatResponse
import streamlit as st
from llama_index import SimpleDirectoryReader, VectorStoreIndex


# TODO: this is caching the resource globally, not per-session
# Each user session should have their own index
@st.cache_resource(show_spinner="Indexing documents...")
def build_index(files):
    documents = SimpleDirectoryReader(input_files=files).load_data()
    return VectorStoreIndex.from_documents(documents)


def handle_stream(root, stream: StreamingAgentChatResponse):
    text = ""
    root.markdown("Thinking...")
    for token in stream.response_gen:
        text += token
        root.markdown(text)
    return text
