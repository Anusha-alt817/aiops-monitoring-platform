from langchain_core.prompts import ChatPromptTemplate

from langchain_rag_retriever import create_retriever


PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an experienced AIOps and DevOps incident investigator.

Analyze the incident using the historical incidents and runbooks
provided in the context.

Do not invent metrics or assume missing data means the application is healthy.

Structure your response using these sections:

1. Incident Summary
2. Evidence from Monitoring
3. Possible Root Causes
4. Recommended Investigation Steps
5. Remediation Suggestions
6. Missing Information

Clearly distinguish confirmed evidence from possible causes.
"""
    ),
    (
        "human",
        """
Incident Question:
{question}

Retrieved Historical Knowledge:
{context}

Analyze this incident using the available evidence.
"""
    )
])


def main():
    question = (
        "API P95 latency is unavailable, but CPU, memory, "
        "and disk usage are normal. What should be investigated?"
    )

    retriever = create_retriever()
    documents = retriever.invoke(question)

    context = "\n\n".join(
        f"Source: {doc.metadata.get('filename')}\n"
        f"Category: {doc.metadata.get('category')}\n"
        f"Content:\n{doc.page_content}"
        for doc in documents
    )

    messages = PROMPT.format_messages(
        question=question,
        context=context
    )

    print("\nLANGCHAIN INCIDENT-ANALYSIS PROMPT")
    print("=" * 60)

    for message in messages:
        print(f"\n[{message.type.upper()}]")
        print(message.content)

    print("\n" + "=" * 60)
    print("Prompt prepared successfully.")
    print("No LLM API call was made.")


if __name__ == "__main__":
    main()
