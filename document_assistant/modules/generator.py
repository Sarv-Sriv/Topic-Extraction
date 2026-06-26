import ollama

from config import (
    LLM_MODEL,
    TEMPERATURE
)


def generate_answer(question, docs, word_count):

    context_sections = []

    used_sources = []

    for i, doc in enumerate(docs, start=1):

        source_text = (
            f"{doc['source']} "
            f"(page {doc['page']})"
        )

        if source_text not in used_sources:
            used_sources.append(source_text)

        section = f"""
SOURCE {i}
File: {doc['source']}
Page: {doc['page']}

Content:
{doc['text']}
"""

        context_sections.append(section)

    context = "\n\n".join(context_sections)

    prompt = f"""
You are an academic research assistant.

Your task is to generate a detailed,
human-like academic response using
information from MULTIPLE provided sources.

STRICT RULES:

1. Use information from multiple sources.
2. Do not rely on only one paper.
3. Write naturally and academically.
4. Avoid robotic repetition.
5. Use clear technical explanations.
6. Expand important concepts properly.
7. Maintain logical flow.
8. Do NOT invent fake citations.
9. Do NOT hallucinate information.
10. After each paragraph add:
(Source: source number, file name, page number)

Target length:
Approximately {word_count} words.

Question:
{question}

DOCUMENTS:
{context}
"""

    try:

        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": TEMPERATURE
            }
        )

        answer = response["message"]["content"]

        answer += "\n\nReferences used:\n"

        for src in used_sources:
            answer += f"- {src}\n"

        return answer

    except Exception as e:

        return f"Model error: {str(e)}"