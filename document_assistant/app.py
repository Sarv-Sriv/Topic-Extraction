from flask import Flask, render_template, request
import os

from config import UPLOAD_FOLDER

from modules.extract_text import (
    extract_pdf,
    extract_docx,
    extract_pptx
)

from modules.chunk_text import split_text

from modules.embeddings import build_index

from modules.retrieval import retrieve_docs

from modules.generator import generate_answer

app = Flask(__name__)

all_documents = []

vector_index = None


def load_documents():

    global all_documents
    global vector_index

    all_documents.clear()

    print("Loading documents...")

    for filename in os.listdir(UPLOAD_FOLDER):

        path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        try:

            if filename.endswith(".pdf"):

                docs = extract_pdf(path)

            elif filename.endswith(".docx"):

                docs = extract_docx(path)

            elif filename.endswith(".pptx"):

                docs = extract_pptx(path)

            else:
                continue

            for doc in docs:

                chunks = split_text(doc["text"])

                for chunk in chunks:

                    all_documents.append({
                        "text": chunk,
                        "source": doc["source"],
                        "page": doc["page"]
                    })

        except Exception as e:

            print(f"Error processing {filename}: {e}")

    print(f"Total chunks: {len(all_documents)}")

    if all_documents:

        vector_index = build_index(all_documents)

        print("Vector index created")


@app.route("/", methods=["GET", "POST"])
def home():

    global vector_index

    answer = ""

    if request.method == "POST":

        question = request.form.get("question")

        word_count = request.form.get("word_count")

        if question and vector_index is not None:

            try:
                word_count = int(word_count)
            except:
                word_count = 500

            docs = retrieve_docs(
                question,
                vector_index,
                all_documents
            )

            answer = generate_answer(
                question,
                docs,
                word_count
            )

    return render_template(
        "index.html",
        answer=answer
    )


if __name__ == "__main__":

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    load_documents()

    app.run(debug=True)