document_assistant
    |-  __pycache__/
    |-  data/
    |    |- uploads/
    |    |- vector_db
    |-  modules/
    |    |- __pycache__/
    |    |- chunk_text.py
    |    |- embeddings.py
    |    |- extract_text.py
    |    |- generator.py
    |    |- retrieval.py
    |-  templates/
    |    |- index.html
    |-  app.py
    |-  config.py
    |-  requirements.txt

The the app.py in termial a local host ID will be given use that to acces, uploads the file in the upload section.
The pdf will be store in document_assistant/data/uploads.

Write a prompt, topic to find on and word count, please enter count less than 400 for accurate result.

requirements.txt contains all the libarary name.
config.py will control the version with the model of LLM, I used OLLAMA qwen2.5:7b, embedding model BAAI/bge-base-en-v1.5, if you compueter can handle change as required and other fields also.

index.html contains is local web page.
