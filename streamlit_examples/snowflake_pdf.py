import streamlit as st
import openai
from llama_index import (
    OpenAIEmbedding,
    ServiceContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
    set_global_service_context,
)
from llama_index.llms import OpenAI

from streamlit_examples.utils.streamlit import (
    cache_file,
    upload_files,
)
from unstructured.partition.pdf import partition_pdf

st.title("☃️ PDF2Snowflake")
st.write("Extracts information from PDFs and stores it in Snowflake.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define service-context
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
embed_model = OpenAIEmbedding()
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
set_global_service_context(service_context)

# Upload PDFs
pdfs = upload_files(type="pdf", accept_multiple_files=True)


# Summarize each PDF
for pdf in pdfs:
    file = cache_file(pdf, type="pdf")
    with st.spinner(f"Indexing '{pdf.name}'..."):
        documents = SimpleDirectoryReader(input_files=[file]).load_data()
        index = VectorStoreIndex.from_documents(documents)
    with st.spinner(f"Summarize '{pdf.name}'..."):
        query_engine = index.as_query_engine()
        summary = query_engine.query("What is a summary of this document?")
    st.markdown(f"## Summary of **{pdf.name}**")
    st.markdown(summary)
    st.markdown("---")
    with st.spinner(f"Extracting tables from '{pdf.name}'..."):
        elements = partition_pdf(filename=file, infer_table_structure=True)
        tables = [el for el in elements if el.category == "Table"]
    for i, table in enumerate(tables):
        html = table.metadata.text_as_html
        st.markdown(f"## Table {i+1} of **{pdf.name}**")
        st.markdown(html, unsafe_allow_html=True)
