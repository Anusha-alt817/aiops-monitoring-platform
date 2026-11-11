from langchain_aws import ChatBedrockConverse
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_incident_prompt import PROMPT
from langchain_rag_retriever import create_retriever
from ai_analysis_writer import save_ai_analysis


REGION = "ap-southeast-2"
MODEL_ID = "au.anthropic.claude-haiku-4-5-20251001-v1:0"


def create_analysis_chain():
    llm = ChatBedrockConverse(
        model=MODEL_ID,
        region_name=REGION,
        max_tokens=800,
        temperature=0
    )

    retriever = create_retriever()

    def get_context(inputs):
        documents = retriever.invoke(inputs["question"])

        return "\n\n".join(
            f"Source: {doc.metadata.get('filename')}\n"
            f"Category: {doc.metadata.get('category')}\n"
            f"Content:\n{doc.page_content}"
            for doc in documents
        )

    chain = (
        RunnablePassthrough.assign(context=get_context)
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain


def main():
    question = (
        "API P95 latency is unavailable, but CPU, memory, "
        "and disk usage are normal. What should be investigated?"
    )

    print("\nLANGCHAIN + AMAZON BEDROCK AIOPS ANALYZER")
    print("=" * 60)
    print("Sending the approved incident-analysis request to Bedrock...")

    chain = create_analysis_chain()
    response = chain.invoke({"question": question})

    print("\n========== AI INCIDENT ANALYSIS ==========")
    print(response)
    save_ai_analysis(question, response)
    print("\n========== ANALYSIS COMPLETED ==========")


if __name__ == "__main__":
    main()
