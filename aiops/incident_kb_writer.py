import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_ROOT / "reports" / "incident_report.json"
INCIDENT_DIR = PROJECT_ROOT / "knowledge_base" / "incidents"


def create_incident_document():
    with REPORT_FILE.open(encoding="utf-8") as file:
        report = json.load(file)

    timestamp = datetime.fromisoformat(report["timestamp"])
    filename = f"auto-incident-{timestamp.strftime('%Y%m%d-%H%M%S')}.md"

    INCIDENT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = INCIDENT_DIR / filename

    lines = [
        "# Automated Historical Incident Report",
        "",
        f"- Project: {report['project']}",
        f"- Timestamp: {report['timestamp']}",
        f"- Status: {report['status']}",
        f"- Alert Count: {report['alert_count']}",
        f"- Insufficient Data Count: {report['insufficient_data_count']}",
        "",
        "## Monitoring Metrics",
        "",
        "| Metric | Endpoint | Value | Threshold | Status |",
        "|---|---|---:|---:|---|"
    ]

    for metric in report["metrics"]:
        lines.append(
            f"| {metric['name']} "
            f"| {metric.get('endpoint') or 'N/A'} "
            f"| {metric.get('value') if metric.get('value') is not None else 'Unavailable'} "
            f"| {metric.get('threshold') if metric.get('threshold') is not None else 'N/A'} "
            f"| {metric['status']} |"
        )

    lines.extend(["", "## Detected Alerts", ""])

    lines.extend(
        [f"- {alert}" for alert in report["detected_alerts"]]
        or ["- No metric alerts detected."]
    )

    lines.extend(["", "## Insufficient Data", ""])

    lines.extend(
        [f"- {item}" for item in report["insufficient_data"]]
        or ["- No unavailable metrics."]
    )

    lines.extend([
        "",
        "## Application Log Analysis",
        "",
        "```text",
        report["log_analysis"].strip(),
        "```",
        "",
        "## Human Validation",
        "",
        "AI-generated findings require human validation before remediation.",
        ""
    ])

    output_file.write_text("\n".join(lines), encoding="utf-8")

    print("Historical incident document created successfully!")
    print(f"File: {output_file.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    create_incident_document()
