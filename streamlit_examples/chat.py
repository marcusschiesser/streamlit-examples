import streamlit as st

from llama_index import (
    OpenAIEmbedding,
    ServiceContext,
    set_global_service_context,
)
from llama_index.llms import OpenAI
from streamlit_examples.utils.llamaindex import build_index, handle_stream

from streamlit_examples.utils.streamlit import (
    get_key,
    render_message,
    upload_files,
)

st.title("Chat with Documents")

openai_api_key = get_key()

# Define service-context
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo", api_key=openai_api_key)
embed_model = OpenAIEmbedding(api_key=openai_api_key)
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
set_global_service_context(service_context)

# Upload PDFs
pdfs = upload_files(type="pdf", accept_multiple_files=True)

index = build_index(pdfs)
query_engine = index.as_chat_engine(chat_mode="condense_question", streaming=True)

messages = st.session_state.get("messages", [])

if not messages:
    messages.append({"role": "assistant", "text": "Hi!"})

for message in messages:
    render_message(message)

if user_query := st.chat_input():
    message = {"role": "user", "text": user_query}
    messages.append(message)
    render_message(message)

    with st.chat_message("assistant"):
        stream = query_engine.stream_chat(user_query)
        text = handle_stream(st.empty(), stream)
        message = {"role": "assistant", "text": text}
        messages.append(message)
        st.session_state.messages = messages
