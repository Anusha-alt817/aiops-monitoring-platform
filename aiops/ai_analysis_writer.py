from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports" / "ai_analysis"


def save_ai_analysis(question, response):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc)

    filename = (
        "ai-incident-"
        + timestamp.strftime("%Y%m%d-%H%M%S")
        + ".md"
    )

    report_path = REPORT_DIR / filename

    report_content = f"""# AI-Generated Incident Analysis

- Project: AI-Powered DevOps Monitoring Platform
- Timestamp (UTC): {timestamp.isoformat()}
- Model: Claude Haiku 4.5
- Framework: LangChain
- Knowledge Source: ChromaDB RAG

## Incident Question

{question}

## AI Incident Analysis

{response}

## Validation

This is AI-generated analysis.
Human validation is required before remediation.
"""

    report_path.write_text(report_content, encoding="utf-8")

    print("\nAI incident report saved successfully!")
    print("File:", report_path.relative_to(PROJECT_ROOT))

    return report_path


if __name__ == "__main__":
    print("AI analysis report writer is ready.")
    print("Report directory:", REPORT_DIR)
