from sentence_transformers import SentenceTransformer
import numpy as np

from config import (
    EMBEDDING_MODEL,
    TOP_K,
    MAX_CONTEXT_CHUNKS
)

model = SentenceTransformer(EMBEDDING_MODEL)


def retrieve_docs(query, index, documents):

    query_vector = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(
        query_vector,
        TOP_K
    )

    results = []

    seen = set()

    for idx in indices[0]:

        if idx >= len(documents):
            continue

        doc = documents[idx]

        unique_key = (
            doc["source"],
            doc["page"],
            doc["text"][:100]
        )

        if unique_key in seen:
            continue

        seen.add(unique_key)

        results.append(doc)

        if len(results) >= MAX_CONTEXT_CHUNKS:
            break

    return results