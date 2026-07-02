import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load catalog
with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f, strict=False)

# Create text for each assessment
documents = []
for item in catalog:
    # Safely get list values
    job_levels = item.get('job_levels', [])
    if not isinstance(job_levels, list):
        job_levels = []
        
    languages = item.get('languages', [])
    if not isinstance(languages, list):
        languages = []
        
    keys = item.get('keys', [])
    if not isinstance(keys, list):
        keys = []

    text = f"""
    Name: {item['name']}
    Type: {item.get('test_type', '')}
    Job Levels: {', '.join(job_levels)}
    Languages: {', '.join(languages)}
    Keys: {', '.join(keys)}
    Description: {item.get('description', '')}
    """
    documents.append(text)

# Generate embeddings
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save index
faiss.write_index(index, "data/faiss.index")

print("Embeddings created successfully for the full enriched catalog!")