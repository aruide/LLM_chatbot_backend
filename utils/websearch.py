from duckduckgo_search import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        snippets = "\n".join([r["body"] for r in results if "body" in r])
    return snippets or "Aucune information trouvée sur le web."