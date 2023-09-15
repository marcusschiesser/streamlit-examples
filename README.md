# streamlit-examples

A couple of AI demo applications built with [Streamlit](https://streamlit.io/):

- [chat.py](./streamlit_examples/chat.py) - Let's the user upload PDF documents and chat with them using LlamaIndex. Supports multiple users and streaming.
- [wiki_search.py](./streamlit_examples/wiki_search.py) - Semantic search over Wikipedia articles using [Weaviate](https://weaviate.io/). Search results are summarized using Cohere. Needs a [Cohere API Key](https://dashboard.cohere.com/api-keys).

## Getting Started

This project uses poetry for dependency management. To install the dependencies and set up the environment, run the following commands:

```bash
# poetry install
# poetry shell
```

You can then run any of the examples by running:

```bash
# streamlit run streamlit_examples/chat.py
```
