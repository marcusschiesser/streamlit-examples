import streamlit as st
from streamlit_examples.utils.cohere import summarize
from streamlit_examples.utils.weaviate import search_wikipedia


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


if "user_query" not in st.session_state:
    st.session_state.user_query = None


def set_query(query):
    st.session_state.user_query = query


def render_suggestions():
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
    user_query = st.chat_input(placeholder="Backpacking in Asia")
    if user_query:
        st.session_state.user_query = user_query


st.title("Search Wikipedia")

if not st.session_state.user_query:
    st.info(
        "Search Wikipedia and summarize the results. Type a query to start or pick one of these suggestions:"
    )
render_suggestions()
render_query()

if not st.session_state.user_query:
    st.stop()

root = st.empty()
with root.status("Querying vector store..."):
    items = search_wikipedia(st.session_state.user_query, limit=10)
# aggregate items with same url (as vector DB might return multiple items for same url)
items = aggregate(items)[0:3]
container = root.container()
container.write(f"That's what I found about: _{st.session_state.user_query}_")

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
