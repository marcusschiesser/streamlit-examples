import streamlit as st
from streamlit_examples.utils.cohere import summarize
from streamlit_examples.utils.weaviate import search_wikipedia


def link(i, item):
    return f"**[{i+1}. {item['title']}]({item['url']})**"


st.title("Search Wikipedia")

user_query = st.chat_input(placeholder="Backpacking in Asia")

if not user_query:
    st.info("Search Wikipedia and summarize the results. Type a query to start.")
    st.stop()

root = st.empty()
with root.status("Querying vector store..."):
    items = search_wikipedia(user_query, limit=3)
container = root.container()
container.write(f"That's what I found about: _{user_query}_")

placeholders = []
for i, item in enumerate(items):
    placeholder = container.empty()
    placeholder.info(f"{link(i,item)} {item['text']}")
    placeholders.append(placeholder)

status = container.status(
    "Search results retrieved. I am summarizing the results for you. Meanwhile you can scroll up and have a look at the full text."
)

for i, item in enumerate(items):
    with placeholders[i].status(f"_Summarizing_: {link(i,item)} {item['text']}"):
        summary = summarize(item["text"])
    placeholders[i].success(f"{link(i,item)} {summary}")

status.update(label="Search finished. Try something else!", state="complete")
