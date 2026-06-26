from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def build_index(documents):

    texts = [doc["text"] for doc in documents]

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    vectors = np.array(vectors).astype("float32")

    dimension = vectors.shape[1]

    # cosine similarity
    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    return index