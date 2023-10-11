import streamlit as st
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

from streamlit_examples.utils.streamlit import (
    cache_file, 
    upload_files,
    initPage,
)

initPage("PDF2Tables")
st.title("PDF2Tables")
st.write("Extracts tables from PDFs using [unstructured](https://unstructured.io/).")

@st.cache_resource()
def get_client():
    return UnstructuredClient(
        security=shared.Security(api_key_auth=st.secrets["UNSTRUCTURED_API_KEY"]),
    )


def extract_elements_api(file):
    req = shared.PartitionParameters(
        # Note that this currently only supports a single file
        files=shared.PartitionParametersFiles(
            content=file.read(),
            files=filename,
        ),
        # Other partition params
        strategy="hi_res",
        pdf_infer_table_structure=True,
    )
    return get_client().general.partition(req).elements


@st.cache_data(show_spinner=False)
def extract_elements(filename):
    with open(filename, "rb") as file:
        try:
            return extract_elements_api(file)
        except SDKError as e:
            st.error(f"Error calling unstructured API: {e.message}")
            return None


# Upload PDFs
pdfs = upload_files(type="pdf", accept_multiple_files=True)


# Extract tables from each PDF
for pdf in pdfs:
    filename = cache_file(pdf, type="pdf")
    with st.spinner(f"Extracting elements from {pdf.name}"):
        elements = extract_elements(filename)

    if elements:
        tables = [el for el in elements if el["type"] == "Table"]
        with st.expander(pdf.name, expanded=True):
            for i, table in enumerate(tables):
                html = table["metadata"]["text_as_html"]
                st.markdown(f"### Table {i+1}:")
                st.markdown(html, unsafe_allow_html=True)
