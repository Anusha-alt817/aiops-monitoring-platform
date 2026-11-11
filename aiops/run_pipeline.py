import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

STEPS = [
    ("Metric anomaly detection and log analysis", "aiops/report_generator.py"),
    ("Historical incident document creation", "aiops/incident_kb_writer.py"),
    ("RAG knowledge-base ingestion", "aiops/rag_ingestion.py"),
]


def run_step(description, script):
    print(f"\n{'=' * 60}")
    print(f"STEP: {description}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        [PYTHON, str(PROJECT_ROOT / script)],
        cwd=PROJECT_ROOT,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at: {description}")


def main():
    print("\nSTARTING AI-POWERED DEVOPS PIPELINE")

    for description, script in STEPS:
        run_step(description, script)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("Incident report generated.")
    print("Historical incident stored.")
    print("ChromaDB knowledge base updated.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nPIPELINE ERROR: {error}")
        sys.exit(1)
