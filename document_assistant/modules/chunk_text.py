from config import CHUNK_SIZE, OVERLAP


def split_text(text):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        chunk_words = words[start:start + CHUNK_SIZE]

        chunk = " ".join(chunk_words).strip()

        if len(chunk) > 100:
            chunks.append(chunk)

        start += CHUNK_SIZE - OVERLAP

    return chunks