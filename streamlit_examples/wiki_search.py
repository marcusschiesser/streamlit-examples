import streamlit as st
from streamlit_examples.utils.cohere import summarize
from streamlit_examples.utils.weaviate import search_wikipedia

from streamlit_examples.utils.theme import (
    initPage,
)

initPage("Search Wikipedia")


def link(i, item):
    return f"**[{i+1}. {item['title']}]({item['url']})**"


def aggregate(items):
    # group items by same url
    groups = {}
    for item in items:
        groups.setdefault(item["url"], []).append(item)
    # join text of same url
    results = []
    for group in groups.values():
        result = {}
        result["url"] = group[0]["url"]  # get url from first item
        result["title"] = group[0]["title"]  # get titl from first item
        result["text"] = "\n\n".join([item["text"] for item in group])
        results.append(result)
    return results


def render_suggestions():
    def set_query(query):
        st.session_state.suggestion = query

    suggestions = [
        "Travel destinations known for their beaches",
        "Time travel movies with a twist",
        "Book authors explaining Physics",
    ]
    columns = st.columns(len(suggestions))
    for i, column in enumerate(columns):
        with column:
            st.button(suggestions[i], on_click=set_query, args=[suggestions[i]])


def render_query():
    st.text_input(
        "Search",
        placeholder="Search, e.g. 'Backpacking in Asia'",
        key="user_query",
        label_visibility="collapsed",
    )


def get_query():
    if "suggestion" not in st.session_state:
        st.session_state.suggestion = None
    if "user_query" not in st.session_state:
        st.session_state.user_query = ""
    user_query = st.session_state.suggestion or st.session_state.user_query
    st.session_state.suggestion = None
    st.session_state.user_query = ""
    return user_query


user_query = get_query()
if not user_query:
    st.info(
        "Search Wikipedia and summarize the results. Type a query to start or pick one of these suggestions:"
    )
render_suggestions()
render_query()

if not user_query:
    st.stop()

MAX_ITEMS = 3

container = st.container()
header = container.empty()
header.write(f"Looking for results for: _{user_query}_")
placeholders = []
for i in range(MAX_ITEMS):
    placeholder = container.empty()
    placeholder.status("Searching...")
    placeholders.append(placeholder)

items = search_wikipedia(user_query, limit=10)
# aggregate items with same url (as vector DB might return multiple items for same url)
items = aggregate(items)[:MAX_ITEMS]

header.write(f"That's what I found about: _{user_query}_. **Summarizing results...**")
for i, item in enumerate(items):
    placeholders[i].info(f"{link(i,item)} {item['text']}")

for i, item in enumerate(items):
    with placeholders[i].status(f"_Summarizing_: {link(i,item)} {item['text']}"):
        summary = summarize(item["text"])
    placeholders[i].success(f"{link(i,item)} {summary}")

header.write("Search finished. Try something else!")
