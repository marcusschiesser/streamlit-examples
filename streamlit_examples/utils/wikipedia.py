from llama_index import Document


def search_wiki(query, lang="en") -> list[Document]:
    try:
        import wikipedia
        from wikipedia import PageError
    except ImportError:
        raise ImportError("Please install wikipedia: poetry add wikipedia")

    wikipedia.set_lang(lang)
    pages = wikipedia.search(query)
    results = []
    for page in pages:
        try:
            wiki_page = wikipedia.page(page, auto_suggest=False)
            results.append(
                Document(
                    text=wiki_page.content,
                    metadata={
                        "title": wiki_page.title,
                        "url": wiki_page.url,
                        "pageid": wiki_page.pageid,
                    },
                )
            )
        except PageError:
            pass
    return results
