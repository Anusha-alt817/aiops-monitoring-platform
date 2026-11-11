import json
import boto3
from pathlib import Path
from rag_retriever import retrieve_context

REGION = "ap-southeast-2"
MODEL_ID = "au.anthropic.claude-haiku-4-5-20251001-v1:0"

INPUT_FILE = Path("reports/incident_report.json")
OUTPUT_FILE = Path("reports/ai_incident_analysis.txt")


def analyze_incident():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Incident report not found: {INPUT_FILE}"
        )

    with INPUT_FILE.open() as file:
        report = json.load(file)

    incident_data = {
        "metrics_analysis": report.get("metrics_analysis", ""),
        "log_analysis": report.get("log_analysis", "")
    }

    # Retrieve relevant historical knowledge from ChromaDB
    search_query = (
        "Troubleshoot banking API application errors, "
        "HTTP 500 failures, slow responses and possible root causes"
    )

    retrieved_documents = retrieve_context(
        search_query,
        n_results=2
    )

    rag_context = "\n\n".join(
        f"SOURCE: {item['source']}\n"
        f"CATEGORY: {item['category']}\n"
        f"CONTENT:\n{item['content']}"
        for item in retrieved_documents
    )

    print("RAG documents retrieved:", len(retrieved_documents))

    prompt = f"""
You are a Senior DevOps Engineer and Site Reliability Engineer.

Analyze the monitoring evidence and retrieved knowledge.

INCIDENT DATA:
{json.dumps(incident_data, indent=2)}

RETRIEVED KNOWLEDGE FROM CHROMADB:
{rag_context}

Perform a structured incident investigation.

1. INCIDENT SUMMARY
Explain the incident and assign severity.

2. OBSERVED EVIDENCE
List confirmed errors, warnings and infrastructure metrics.
Never treat missing or NaN metrics as zero.

3. ROOT CAUSE ANALYSIS
Separate confirmed facts from hypotheses.
Use historical incidents only as supporting reference,
not as proof of the current root cause.

4. TROUBLESHOOTING ACTIONS
Provide practical Linux, Docker and application debugging commands.
Do not execute commands or modify infrastructure.

5. PREVENTION RECOMMENDATIONS
Suggest monitoring, alerting and logging improvements.

IMPORTANT:
- Use only supplied evidence and retrieved knowledge.
- Do not invent infrastructure failures.
- Do not claim correlation proves causation.
- Clearly identify missing evidence.
- Human validation is mandatory.
- Keep the response within 800 tokens.
"""

    client = boto3.client(
        "bedrock-runtime",
        region_name=REGION
    )

    print("\nSending incident report and RAG context to Amazon Bedrock...")

    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        inferenceConfig={
            "maxTokens": 800,
            "temperature": 0.2
        }
    )

    analysis = response["output"]["message"]["content"][0]["text"]
    usage = response.get("usage", {})

    OUTPUT_FILE.write_text(analysis + "\n")

    print("\n========== AI INCIDENT ANALYSIS ==========")
    print(analysis)

    print("\n========== TOKEN USAGE ==========")
    print("Input tokens:", usage.get("inputTokens", "N/A"))
    print("Output tokens:", usage.get("outputTokens", "N/A"))

    print("\nAI analysis saved to:", OUTPUT_FILE)
    print("Human validation is required before taking action.")


if __name__ == "__main__":
    try:
        analyze_incident()

    except Exception as error:
        print("\nBedrock analysis failed:")
        print(error)
