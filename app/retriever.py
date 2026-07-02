import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss.index")

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f, strict=False)


def retrieve(query, messages=None, k=30):
    """
    Retrieve relevant assessments from the catalog using hybrid search:
    1. Vector search on the current query.
    2. Vector search on all user messages combined.
    3. Direct name/URL matching of items mentioned in conversation history.
    """
    results = []
    seen_urls = set()

    def add_item(item):
        url = item.get('url')
        if url and url not in seen_urls:
            seen_urls.add(url)
            results.append(item)

    # 1. Vector search on current query
    if query:
        emb = model.encode([query])
        D, I = index.search(np.array(emb).astype("float32"), min(k, len(catalog)))
        for idx in I[0]:
            if 0 <= idx < len(catalog):
                add_item(catalog[idx])

    # 2. Vector search on combined user queries
    if messages:
        user_queries = [m.get("content", "") for m in messages if m.get("role") == "user"]
        if user_queries:
            combined_query = " ".join(user_queries)
            emb = model.encode([combined_query])
            D, I = index.search(np.array(emb).astype("float32"), min(k, len(catalog)))
            for idx in I[0]:
                if 0 <= idx < len(catalog):
                    add_item(catalog[idx])

    # 3. Direct matching of catalog item names or URLs mentioned in conversation history
    if messages:
        # Concatenate all messages (user + assistant) to scan
        full_history = " ".join([m.get("content", "") for m in messages]).lower()
        for item in catalog:
            name = item.get('name', '')
            url = item.get('url', '')
            
            # Match exact URL or clean name in history
            if url and url.lower() in full_history:
                add_item(item)
            else:
                name_lower = name.lower()
                # Check for direct inclusion of name
                if name_lower in full_history:
                    add_item(item)
                # Specific common abbreviations used in traces
                elif "opq" in name_lower and "opq" in full_history:
                    add_item(item)
                elif "verify g+" in name_lower and ("g+" in full_history or "verify g" in full_history):
                    add_item(item)
                elif "gsa" in name_lower and "gsa" in full_history:
                    add_item(item)
                elif "dsi" in name_lower and "dsi" in full_history:
                    add_item(item)

    return results