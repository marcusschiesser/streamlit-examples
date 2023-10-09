import streamlit as st
from unstructured.partition.pdf import partition_pdf

from streamlit_examples.utils.streamlit import cache_file, upload_files

st.title("PDF2Tables")
st.write("Extracts tables from PDFs using [unstructured](https://unstructured.io/).")

# Upload PDFs
pdfs = upload_files(type="pdf", accept_multiple_files=True)


# Extract tables from each PDF
for pdf in pdfs:
    file = cache_file(pdf, type="pdf")

    with st.spinner(f"Extracting tables from '{pdf.name}'..."):
        elements = partition_pdf(
            filename=file,
            strategy="hi_res",
            infer_table_structure=True,
        )
        tables = [el for el in elements if el.category == "Table"]
    for i, table in enumerate(tables):
        html = table.metadata.text_as_html
        st.markdown(f"## Table {i+1} of **{pdf.name}**")
        st.markdown(html, unsafe_allow_html=True)
